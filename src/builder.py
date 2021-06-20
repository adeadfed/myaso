import json
import os.path
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field

import chevron
from colorama import Style, Fore
from yaml import safe_load
from loguru import logger

from src.ps_minifier import minify_PS

@dataclass
class Runner:
    """Payload runner. Used as a config for Builder"""
    name: str
    os: str
    arch: str

    language: str
    payload: str
    algorithm: str

    image_source: str = field(default_factory=str)
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
            logger.info(f'Usage: {runner.name}.{builder.build_extension} {kwargs["BYTE_LENGTH"]} {kwargs["PAYLOAD_SOURCE"]}')
        else:
            logger.info(f'Usage: {runner.name}.{builder.build_extension} PAYLOAD_SIZE PAYLOAD_SOURCE')


class Builder:
    """A language-specific templating engine"""
    sources_extension = ''
    build_extension = 'exe'
    build_dir = '.'

    CLASS_MAPPING_FILE = 'class_mapping.json'

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
        with open(f'{self.main_file}.mst') as template:
            script = chevron.render(template, self.runner.params)
            with open(f'{self.main_file}', 'w') as f:
                f.write(script)

    @property
    def main_file(self):
        return f'runner.{self.sources_extension}'

    def run_build(self):
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
            os.chdir(self.build_dir)
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
            os.chdir(old_cwd)

        return success

    @classmethod
    def from_runner(cls, runner: Runner):
        logger.debug('Finding you a template...')
        implementations = {
            'cpp': CppBuilder,
            'csharp': CSharpBuilder,
            'go': GoBuilder,
            'powershell': PowershellBuilder,
            'vba': VbaBuilder
        }
        try:
            return implementations[runner.language](runner)
        except KeyError:
            logger.error(f'Runner in {runner.language} not found')
            exit(-1)

    def add_class_map_to_template_arguments(self):
        with open(self.CLASS_MAPPING_FILE) as f:
            class_mapping = json.loads(f.read())

        self.runner.params.update({
            'image_source': class_mapping['image_sources'][self.runner.image_source],
            'payload': class_mapping['payloads'][self.runner.payload],
            'algorithm': self.runner.algorithm
        })

        try:
            args = self.runner.params['args']
            self.runner.params.update({
                'image_source_args': args.get('image_source'),
                'algorithm_args': args.get('algorithm'),
                'payload_args': args.get('payload'),
            })
        except KeyError:
            pass


class CppBuilder(Builder):
    sources_extension = 'cpp'
    build_dir = 'cpp'
    compilers = {
        'x86': '/usr/bin/i686-w64-mingw32-g++',
        'x64': '/usr/bin/x86_64-w64-mingw32-g++'
    }
    libs = defaultdict(list, {
        'remote': ['winhttp', 'ole32'],
    })

    def preprocess_sources(self):
        self.add_class_map_to_template_arguments()
        super().preprocess_sources()

    def run_build(self):
        libs = ['gdiplus'] + self.libs[self.runner.image_source] + self.libs[self.runner.payload]
        libs = set(libs)
        libs = ' '.join(f'-l{lib} -Wl,-Bstatic' for lib in libs)
        cmd = (
            f'{self.compilers[self.runner.arch]} '
            f'{self.main_file} '
            f'-s -static-libgcc -static-libstdc++ '
            f'{libs} '
            f'-Wall '
            f'-municode '
            f'-o {self.runner.name}.{self.build_extension}'
        )
        logger.debug(os.getcwd())
        logger.debug(cmd)
        assert (o := subprocess.run(cmd, shell=True, capture_output=True)).returncode == 0, \
            b'\\n'.join([o.stdout, o.stderr]).decode("unicode_escape")


class CSharpBuilder(Builder):
    sources_extension = 'cs'
    build_dir = 'csharp'

    def preprocess_sources(self):
        self.add_class_map_to_template_arguments()
        super().preprocess_sources()

    def run_build(self):
        logger.debug(os.getcwd())
        cmd = (
            f'mcs -platform:{self.runner.arch} '
            f'/reference:System.Drawing '
            f'{self.runner.name}.{self.sources_extension} '
            f'./Algorithms/* ./Payloads/* ./ImageSources/*'
        )
        logger.debug(cmd)
        assert (o := subprocess.run(cmd, shell=True, capture_output=True)).returncode == 0, (o.stdout, o.stderr)


class GoBuilder(Builder):
    build_dir = '.'
    sources_extension = 'go'
    architectures = {
        'x86': '386',
        'x64': 'amd64'
    }

    def preprocess_sources(self):
        self.add_class_map_to_template_arguments()
        super().preprocess_sources()

    def run_build(self):
        o = subprocess.run(
            f'go build -ldflags "-s -w" -o {self.runner.name}.{self.build_extension}',
            shell=True,
            env=os.environ.update({
                'GOARCH': self.architectures[self.runner.arch],
                'GOOS': 'windows'
            }),
            capture_output=True
        )
        if o.returncode:
            raise RuntimeError(o.stderr)


class PowershellBuilder(Builder):
    sources_extension = 'ps1'
    build_extension = sources_extension

    def preprocess_sources(self):
        with open(f'algorithms/{self.runner.algorithm.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'ALGORITHM_CODE': chevron.render(f.read(), self.runner.params)})

        with open(f'image_sources/{self.runner.image_source.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'PAYLOAD_DELIVERY_CODE': chevron.render(f.read(), self.runner.params)})

        with open(f'payloads/{self.runner.payload.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'PAYLOAD_EXEC_CODE': chevron.render(f.read(), self.runner.params)})

        super().preprocess_sources()

        with open(f'{self.main_file}', 'r') as f:
            script = f.read()

        with open(f'{self.main_file}', 'w') as f:
            f.write(minify_PS(script))


class VbaBuilder(Builder):
    sources_extension = 'vba'
    build_extension = sources_extension

    def preprocess_sources(self):
        with open(f'algorithms/{self.runner.algorithm.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'ALGORITHM_CODE': chevron.render(f.read(), self.runner.params)})
        
        with open(f'arches/{self.runner.arch.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'ARCH_IMPORTS': chevron.render(f.read(), self.runner.params)})

        with open(f'payloads/{self.runner.payload.lower()}_{self.runner.arch.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'PAYLOAD_CODE': chevron.render(f.read(), self.runner.params)})

        return super().preprocess_sources()