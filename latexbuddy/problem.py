"""This module describes the LaTeXBuddy Problem class and its properties.

*Problems* are found by *Checkers*. *Checkers* are free to implement their own Problem
types, however LaTeXBuddy will most probably not display extra metadata.
"""

import time

from enum import Enum
from functools import total_ordering
from json import JSONEncoder
from pathlib import Path
from typing import Any, List, Optional, Tuple


@total_ordering
class ProblemSeverity(Enum):
    """Defines possible problem severity grades.

    Problem severity is usually preset by the checkers themselves. However, a user
    should be able to redefine the severity of a specific problem, using either
    category, key, or p_type.

    * "none" problems are not being highlighted, but are still being output.
    * "info" problems are highlighted with light blue colour. These are suggestions;
      problems, that aren't criticising the text.
      Example: suggestion to use "lots" instead of "a lot"
    * "warning" problems are highlighted with orange colour. These are warnings about
      problematic areas in documents. The files compile and work as expected, but some
      behaviour may be unacceptable.
      Example: warning about using "$$" in LaTeX
    * "error" problems are highlighted with red colour. These are errors, that prevent
      the documents to compile correctly.
      Example: not closed environment, or wrong LaTeX syntax
    """

    NONE = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    def __str__(self):
        return self.name.lower()

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value


class Problem:
    """Describes a Problem object.

    A Problem object contains information about a problem detected by a checker. For
    example, it can be wrong LaTeX code or a misspelled word.
    """

    def __init__(
        self,
        position: Optional[Tuple[int, int]],
        text: str,
        checker: str,
        file: Path,
        severity: ProblemSeverity = ProblemSeverity.WARNING,
        p_type: Optional[str] = None,
        length: Optional[int] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        context: Optional[Tuple[str, str]] = None,
        suggestions: Optional[List[str]] = None,
        key: Optional[str] = None,
    ):
        """

        :param position: position of the problem in the source file, encoded as
                         `(line, column)`.
        :param length: the length of the problematic text.
        :param text: problematic text.
        :param checker: name of the tool that discovered the problem.
        :param p_type: ID of the problem type, used inside the respective checker.
        :param file: **[DEPRECATED]** path to the file where the problem was found
        :param severity: severity of the problem.
        :param category: category of the problem, for example "grammar".
        :param description: description of the problem.
        :param context: optional context of the problem, that is, text that comes before
                        and after the problematic text.
        :param suggestions: list of suggestions, that is, possible replacements for
                            problematic text.
        :param key: semi-unique string, which can be used to compare two problems. Will
                    be used for entries in the whitelist

        """
        self.position = position
        if length is None:
            length = 0
        self.length = length
        self.text = text
        self.checker = checker
        if p_type is None:
            p_type = ""
        self.p_type = p_type
        self.file = file  # FIXME: deprecated!
        self.severity = severity
        self.category = category
        self.description = description
        if context is None:
            context = ("", "")
        self.context = context
        if suggestions is None:
            suggestions = []
        self.suggestions = suggestions
        self.key = key

        if self.key is None:
            self.key = self.__generate_key()
        self.length = len(text)
        self.uid = self.__generate_uid()

    def __generate_key(self) -> str:
        """Generates a key for the problem based on checker and problematic text.

        This method is particularly used in the constructor for the cases when the key
        wasn't previously supplied.

        :return: generated key
        """
        return f"{self.checker}/{self.p_type}/{self.text}"

    def __generate_uid(self) -> str:
        """ Creates the UID for the Problem object.

        :return: a unique UID for the Problem object
        """
        return str(time.time())

    def __get_pos_str(self) -> str:
        """Returns the string value of the problem's position.

        :return: string value of the position
        """
        if self.position is None:
            return "None"

        return f"{self.position[0]}:{self.position[1]}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Problem):
            return False

        if not self.key or not o.key:
            return False

        return self.key == o.key

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __str__(self) -> str:
        return (
            f"{str(self.category).capitalize()} "
            f"{str(self.severity).lower()} "
            f"on {self.__get_pos_str()}: "
            f"{self.text}: "
            f"{self.description}."
        )


class ProblemJSONEncoder(JSONEncoder):
    """Provides JSON serializability for class Problem"""

    def default(self, obj: Any):

        if type(obj) == Problem:

            return {
                "position": obj.position,
                "text": obj.text,
                "checker": obj.checker,
                "p_type": obj.p_type,
                "file": str(obj.file),
                "severity": str(obj.severity),
                "length": obj.length,
                "category": obj.category,
                "description": obj.description,
                "context": obj.context,
                "suggestions": obj.suggestions,
                "key": obj.key,
            }

        else:
            return JSONEncoder.default(self, obj)
