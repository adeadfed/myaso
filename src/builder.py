import os.path
from dataclasses import dataclass

import chevron
from yaml import safe_load


@dataclass
class Runner:
    """Shellcode runner. Knows how to build itself"""
    method: str
    language: str
    algorithm: str
    options: dict

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as f:
            return cls(**safe_load(f))

    @property
    def sources(self):
        return os.path.join('readers', self.language, self.method)


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
        try:
            os.mkdir('build')
        except FileExistsError:
            pass

        self.preprocess_sources()
        self.run_build()

        os.chdir(old_cwd)

    @classmethod
    def from_runner(cls, runner: Runner):
        implementations = {
            # 'c': CBuilder,
            # 'csharp': CSharpBuilder,
            # 'go': GoBuilder,
            'powershell': PowershellBuilder,
            # 'rust': RustBuilder
        }
        return implementations[runner.language](runner)


class PowershellBuilder(Builder):
    def preprocess_sources(self):
        with open('template.ps1') as template:
            script = chevron.render(template, self.runner.options)
            with open(os.path.join('build', 'runner.ps1'), 'w') as f:
                f.write(script)

    def run_build(self):
        pass
