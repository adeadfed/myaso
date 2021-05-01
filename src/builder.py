import os.path
from collections import defaultdict
from shutil import copy
from dataclasses import dataclass

import chevron
from yaml import safe_load
from loguru import logger


@dataclass
class Runner:
    """Shellcode runner. Knows how to build itself"""
    name: str
    os: str
    arch: str

    language: str
    delivery_method: str
    payload_type: str
    algorithm: str

    params: dict

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            return cls(**safe_load(f))

    @property
    def sources(self):
        return os.path.join('readers', self.language)

    def __str__(self):
        return f'{self.name} ({self.os}/{self.arch}/{self.language}/{self.payload_type}, ' \
               f'algorithm={self.algorithm}, params={self.params})'


def get_runner(runner_config: str):
    runner = Runner.from_file(runner_config)
    builder = Builder.from_runner(runner)

    logger.success('Builder configured')
    logger.info(f'Configuration: {runner}')
    builder.build()
    logger.artifact(f'Runner is at {builder.artifact_path}')
    logger.info(f'Usage: {runner.name} stego')


class Builder:
    template_file = ''
    build_dir = 'build'

    def __init__(self, runner: Runner):
        self.runner = runner

    @property
    def artifact_path(self) -> str:
        return os.path.join(self.runner.sources, self.build_dir, self.runner.name)

    def preprocess_sources(self):
        with open(self.template_file) as template:
            script = chevron.render(template, self.runner.params)
            with open(os.path.join(self.build_dir, self.runner.name), 'w') as f:
                f.write(script)

    def run_build(self):
        pass

    def build(self):
        old_cwd = os.getcwd()
        os.chdir(self.runner.sources)
        try:
            os.mkdir(self.build_dir)
        except FileExistsError:
            pass

        logger.debug('Preparing the sources...')
        self.preprocess_sources()

        logger.info('Starting the build...')
        self.run_build()
        logger.success('Build was successful!')

        os.chdir(old_cwd)

    @classmethod
    def from_runner(cls, runner: Runner):
        logger.debug('Finding you a template...')
        implementations = {
            'c': CBuilder,
            'csharp': CSharpBuilder,
            'go': GoBuilder,
            'powershell': PowershellBuilder,
        }
        try:
            return implementations[runner.language](runner)
        except KeyError:
            logger.error(f'Runner in {runner.language} not found')


class CBuilder(Builder):
    template_file = 'c/Source.cpp'
    compilers = {
        'x86': '/usr/bin/i686-w64-mingw32-g++',
        'x64': '/usr/bin/x86_64-w64-mingw32-g++'
    }
    libs = defaultdict(list, {
        'remote': ['winhttp', 'ole32'],
        'cmd': ['gdiplus'],
        'shellcode': ['gdiplus'],
    })

    def run_build(self):
        libs = self.libs[self.runner.delivery_method] + self.libs[self.runner.payload_type]
        libs = set(libs)
        libs = ' '.join(f'-l{lib} -Wl,-Bstatic' for lib in libs)
        os.popen(
            f'{self.compilers[self.runner.arch]} '
            f'{self.template_file} '
            f'-s -static-libgcc -static-libstdc++ '
            f'{libs} '
            f'-Wall '
            f'-o {self.build_dir}/{self.runner.name}'
        )


class CSharpBuilder(Builder):
    template_file = 'csharp/Program.cs'

    def build(self):
        os.popen(f'mcs -platform:{self.runner.arch} -reference:System.Drawing {self.build_dir}/{self.runner.name}')


class GoBuilder(Builder):
    template_file = 'template.go'

    def preprocess_sources(self):
        super(self).preprocess_sources()
        for file in ['go.mod', 'go.sum']:
            copy(file, 'build')

    def run_build(self):
        os.chdir(self.build_dir)
        os.popen('go build')


class PowershellBuilder(Builder):
    template_file = 'template.ps1'

    def preprocess_sources(self):
        with open(f'algorithms/{self.runner.algorithm.lower()}') as f:
            self.runner.params.update({'ALGORITHM_CODE': f.read()})
        with open(f'delivery_methods/{self.runner.delivery_method.lower()}') as f:
            self.runner.params.update({'PAYLOAD_DELIVERY_CODE': f.read()})
        with open(f'payload_types/{self.runner.payload_type.lower()}') as f:
            self.runner.params.update({'PAYLOAD_EXEC_CODE': f.read()})

        super().preprocess_sources()
