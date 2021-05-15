"""This module descibes the main LaTeXBuddy instance class."""

import json
import os

import latexbuddy.abstractmodules as abstract
import latexbuddy.tools as tools

from latexbuddy.error_class import Error


# FIXME: rename this file (e.g. to 'buddy') because it's confusing

# TODO: make this a singleton class with static methods


class LatexBuddy:
    """The main instance of the applications that controls all the internal tools."""

    # TODO: use pathlib.Path
    def __init__(
        self, error_file: str, whitelist_file: str, file_to_check: str, lang: str
    ):
        """Initializes the LaTeXBuddy instance.

        :param error_file: path to the file where the error should be saved
        :param whitelist_file: path to the whitelist file
        :param file_to_check: file that will be checked
        :param lang: language of the file
        """
        self.errors = {}  # all current errors
        self.error_file = error_file
        self.whitelist_file = whitelist_file
        self.file_to_check = file_to_check
        self.lang = lang

    def add_error(self, error: Error):
        """Adds the error to the errors dictionary.

        UID is used as key, the error object is used as value.

        :param error: error to add to the dictionary
        """

        self.errors[error.get_uid()] = error

    # TODO: rename method. Parse = read; this method writes
    # TODO: maybe remove the method completely
    def parse_to_json(self):
        """Writes all the current error objects into the error file."""

        # TODO: extend JSONEncoder to get rid of such hacks
        with open(self.error_file, "w+") as file:
            file.write("[")
            uids = list(self.errors.keys())
            for uid in uids:
                json.dump(self.errors[uid].__dict__, file, indent=4)
                if not uid == uids[-1]:
                    file.write(",")

            file.write("]")

    def check_whitelist(self):
        """Remove errors that are whitelisted."""
        if not os.path.isfile(self.whitelist_file):
            return  # if no whitelist yet, don't have to check

        with open(self.whitelist_file, "r") as file:
            whitelist = file.read().split("\n")

        for whitelist_element in whitelist:
            uids = list(self.errors.keys())
            for uid in uids:
                if self.errors[uid].compare_with_other_comp_id(whitelist_element):
                    del self.errors[uid]

    def add_to_whitelist(self, uid):
        """Adds the error identified by the given UID to the whitelist

        Afterwards this method deletes all other errors that are the same as the one
        just whitelisted.

        :param uid: the UID of the error to be deleted
        """

        if uid not in self.errors.keys():
            print(
                "Error: invalid UID, error object with ID: "
                + uid
                + "not found and not added to whitelist"
            )
            return

        # write error in whitelist
        with open(self.whitelist_file, "a+") as file:
            file.write(self.errors[uid].get_comp_id())
            file.write("\n")

        # delete error and save comp_id for further check
        compare_id = self.errors[uid].get_comp_id()
        del self.errors[uid]

        # check if there are other errors equal to the one just added to the whitelist
        uids = list(self.errors.keys())
        for curr_uid in uids:
            if self.errors[curr_uid].compare_with_other_comp_id(compare_id):
                del self.errors[curr_uid]

    # TODO: implement
    # def add_to_whitelist_manually(self):
    #     return

    def run_tools(self):
        """Runs all tools in the LaTeXBuddy toolchain"""
        # check_preprocessor
        # check_config

        # with abstractmodules
        chktex = abstract.Chktex()
        chktex.run(self, self.file_to_check)
        detexed_file = tools.detex(self.file_to_check)
        aspell = abstract.Aspell()
        aspell.run(self, detexed_file)
        languagetool = abstract.Languagetool()
        languagetool.run(self, detexed_file)

        # without abstractmodules
        """"
        chktex.run(self, self.file_to_check)
        detexed_file = tools.detex(self.file_to_check)
        aspell.run(self, detexed_file)
        languagetool.run(self, detexed_file)
        """

        # FOR TESTING ONLY

        """
        self.check_whitelist()
        keys = list(self.errors.keys())
        for key in keys:
            self.add_to_whitelist(key)
            return
        """

        # TODO: use tempfile.TemporaryFile instead
        os.remove(detexed_file)

    # TODO: why does this exist? Use direct access
    def get_lang(self) -> str:
        """Returns the set LaTeXBuddy language.

        :returns: language code
        """
        return self.lang
