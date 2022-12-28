# LaTeXBuddy tests
# Copyright (C) 2021-2022  LaTeXBuddy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import annotations

from latexbuddy.config_loader import ConfigLoader
from latexbuddy.modules import Module
from latexbuddy.problem import Problem
from latexbuddy.problem import ProblemSeverity
from latexbuddy.texfile import TexFile


class FirstDriver(Module):
    def __init__(self):
        pass

    def run_checks(self, config: ConfigLoader, file: TexFile) -> list[Problem]:
        problems = [
            Problem(
                position=None,
                text="just a general problem",
                checker=FirstDriver,
                file=file.plain_file,
                severity=ProblemSeverity.ERROR,
            ),
        ]

        abs_pos = str(file.plain).find("This is")
        problems.append(
            Problem(
                position=file.get_position_in_tex(abs_pos),
                text="This is",
                checker=FirstDriver,
                file=file.plain_file,
                severity=ProblemSeverity.ERROR,
                description="Not an actual error, just testing the software...",
            ),
        )

        return problems
