from typing import List

from latexbuddy.config_loader import ConfigLoader
from latexbuddy.log import Loggable
from latexbuddy.module_loader import ModuleProvider
from latexbuddy.modules import Module
from latexbuddy.problem import Problem, ProblemSeverity
from latexbuddy.texfile import TexFile


class DriverModuleProvider(ModuleProvider, Loggable):

    def load_selected_modules(self, cfg: ConfigLoader) -> List[Module]:
        return self.load_modules()

    def load_modules(self) -> List[Module]:
        self.logger.debug("Returning scripted module instances.")
        return [DriverModule0(), DriverModule1()]


class DriverModule0(Module):

    def __init__(self):
        return

    def run_checks(self, config: ConfigLoader, file: TexFile) -> List[Problem]:
        self.logger.debug("returning no problems")
        return []


class DriverModule1(Module):

    def __init__(self):
        return

    def run_checks(self, config: ConfigLoader, file: TexFile) -> List[Problem]:
        return [
            Problem(
                position=None,
                text="just a general problem",
                checker=DriverModule1,
                file=file.plain_file,
                severity=ProblemSeverity.INFO
            )
        ]