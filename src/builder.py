import os.path
from dataclasses import dataclass
from yaml import safe_load


@dataclass
class Runner:
    """Shellcode runner. Knows how to build itself"""
    mode: str
    language: str
    delivery_method: str
    algorithm: str

    @classmethod
    def from_file(cls, filename: str):
        return cls(**safe_load(filename))

    @property
    def sources(self):
        return os.path.join('readers', self.mode, self.language)


def get_runner(runner_config: str):
    runner = Runner.from_file(runner_config)
    Builder.from_runner(runner).build()


class Builder:
    def __init__(self, runner: Runner):
        self.runner = runner

    def preprocess_sources(self):
        raise NotImplementedError

    def run_build(self):
        raise NotImplementedError

    def build(self):
        old_cwd = os.getcwd()
        os.chdir(self.runner.sources)

        os.mkdir('build')
        self.preprocess_sources()
        self.run_build()

        os.chdir(old_cwd)

    @classmethod
    def from_runner(cls, runner: Runner):
        implementations = {}
        return implementations[runner.language](runner)

