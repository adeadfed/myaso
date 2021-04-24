import os.path
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
        return os.path.join('readers', self.language, self.payload_type)

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
    def __init__(self, runner: Runner):
        self.runner = runner
        self.build_dir = 'build'

    @property
    def artifact_path(self) -> str:
        return os.path.join(self.runner.sources, self.build_dir, self.runner.name)

    def preprocess_sources(self):
        raise NotImplementedError

    def run_build(self):
        raise NotImplementedError

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
            # 'c': CBuilder,
            # 'csharp': CSharpBuilder,
            'go': GoBuilder,
            'powershell': PowershellBuilder,
        }
        try:
            return implementations[runner.language](runner)
        except KeyError:
            logger.error(f'Runner in {runner.language} not found')


class GoBuilder(Builder):
    def preprocess_sources(self):
        with open('template.go') as template:
            script = chevron.render(template, self.runner.params)
            with open(os.path.join(self.build_dir, 'runner.go'), 'w') as f:
                f.write(script)

        for file in ['go.mod', 'go.sum']:
            copy(file, 'build')

    def run_build(self):
        os.chdir(self.build_dir)
        os.popen('go build')


class PowershellBuilder(Builder):
    def preprocess_sources(self):
        with open('template.ps1') as template:
            script = chevron.render(template, self.runner.params)
            with open(os.path.join(self.build_dir, self.runner.name), 'w') as f:
                f.write(script)

    def run_build(self):
        pass
