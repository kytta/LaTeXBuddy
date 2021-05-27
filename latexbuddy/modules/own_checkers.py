import re

import latexbuddy.tools as tools

from latexbuddy.buddy import LatexBuddy
from latexbuddy.modules import Module
from latexbuddy.problem import Problem, ProblemSeverity
from latexbuddy.texfile import TexFile


class UnreferencedFiguresModule(Module):
    def __init__(self):
        self.tool_name = "refcheck"
        self.cid = "0"
        self.severity = ProblemSeverity.INFO
        self.category = "latex"

    def run_checks(self, buddy: LatexBuddy, file: TexFile) -> list[Problem]:
        """Finds unreferenced figures.
        :param: buddy: the buddy instance
        :param: file: the file to check
        :return: a list of found problems
        """
        tex = file.tex
        problems = []
        # key = self.tool_name + '_' + fig_num
        pattern = r"\\begin{figure}[\w\W]*?\\end{figure}"
        figures = re.findall(pattern, tex)
        len_label = len("label{")
        labels = {}
        for figure in figures:
            match = re.search(re.escape(figure), tex)
            absolute_position = match.span()[0]
            length = match.span()[1] - match.span()[0]
            split = figure.split("\\")
            for word in split:
                if (
                    re.search(re.escape("label{") + ".*" + re.escape("}"), word)
                    is not None
                ):
                    label = word[len_label : len(word) - 2]
                    labels[label] = (absolute_position, length)
        for label in labels.keys():
            pos_len = labels[label]
            position = pos_len[0]
            length = pos_len[1]
            line, col, offset = tools.absolute_to_linecol(file.tex, position)
            if re.search(re.escape("\\ref{") + label + re.escape("}"), tex) is None:
                problems.append(
                    Problem(
                        position=(line, col),
                        text=label,
                        checker=self.tool_name,
                        category=self.category,
                        cid=self.cid,
                        file=file.tex_file,
                        severity=self.severity,
                        description=f"Figure {label} not referenced.",
                        key=self.tool_name + "_" + label,
                        length=length,
                        context=("\\label{", "}"),
                    )
                )

        return problems


class SiUnitxModule(Module):
    def __init__(self):
        self.tool_name = "siunitx"
        self.category = "latex"
        self.severity = ProblemSeverity.INFO

    def run_checks(self, buddy: LatexBuddy, file: TexFile) -> list[Problem]:
        """Finds units and long numbers used without siunitx package.
        :param: buddy: the buddy instance
        :param: file: the file to check
        :return: a list of found problems
        """
        problems = []
        text = file.tex
        for problem in self.find_long_numbers(file):
            problems.append(problem)
        for problem in self.find_units(file):
            problems.append(problem)
        return problems

    def find_long_numbers(self, file: TexFile) -> list[Problem]:
        """Finds long numbers used without siunitx package.
        :param: file: the file to check
        :return: a list of found problems
        """
        problems = []
        text = file.tex
        all_numbers = re.findall("[0-9]+", text)
        threshold = 3

        def filter_big_numbers(n):
            return True if len(n) > threshold else False

        numbers = list(filter(filter_big_numbers, all_numbers))

        for number in numbers:
            match = re.search(re.escape(str(number)), text)
            start, end = match.span()
            length = end - start
            line, col, offset = tools.absolute_to_linecol(text, start)
            problems.append(
                Problem(
                    position=(line, col),
                    text=str(number),
                    checker=self.tool_name,
                    category=self.category,
                    cid="num",
                    file=file.tex_file,
                    severity=self.severity,
                    description=f"For number {number} \\num from siunitx may be used.",
                    key=self.tool_name + "_" + str(number),
                    length=length,
                )
            )
        return problems

    def find_units(self, file: TexFile) -> list[Problem]:
        """Finds units used without siunitx package.
        :param: file: the file to check
        :return: a list of found problems
        """
        problems = []
        units = [
            "A",
            "cd",
            "K",
            "kg",
            "m",
            "mol",
            "s",
            "C",
            "F",
            "Gy",
            "Hz",
            "H",
            "J",
            "lm",
            "kat",
            "lx",
            "N",
            "Pa",
            "rad",
            "S",
            "Sv",
            "sr",
            "T",
            "V",
            "W",
            "Wb",
            "au",
            "B",
            "Da",
            "d",
            "dB",
            "eV",
            "ha",
            "h",
            "L",
            "min",
            "Np",
            "t",
        ]
        prefixes = [
            "y",
            "z",
            "a",
            "f",
            "p",
            "n",
            "m",
            "c",
            "d",
            "da",
            "h",
            "k",
            "M",
            "G",
            "T",
            "P",
            "E",
            "Z",
            "Y",
        ]
        text = file.tex
        units_cp = units.copy()
        for unit in units:
            for prefix in prefixes:
                units_cp.append(prefix + unit)

        units = units_cp.copy()

        used_units = []
        for unit in units:
            pattern = rf"[0-9]+\s*{unit}"
            used_unit = re.findall(pattern, text)
            used_units.append(used_unit)

        for used_unit in used_units:
            for unit in used_unit:
                match = re.search(re.escape(unit), text)
                start, end = match.span()
                length = end - start
                line, col, offset = tools.absolute_to_linecol(text, start)
                problems.append(
                    Problem(
                        position=(line, col),
                        text=unit,
                        checker=self.tool_name,
                        category=self.category,
                        cid="unit",
                        file=file.tex_file,
                        severity=self.severity,
                        description=f"For unit {unit} siunitx may be used.",
                        key=self.tool_name + "_" + unit,
                        length=length,
                    )
                )

        return problems
