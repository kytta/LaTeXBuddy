import json
import os

import chktex
import aspell
import tools


class LatexBuddy:
    def __init__(self, lang):
        self.errors = {}
        self.error_file = "errors.json"
        self.whitelist_file = "whitelist.json"
        self.file_to_check = "Test.tex"
        self.lang = lang

    def add_error(self, error):
        self.errors[error.get_uid()] = error

    def parse_to_json(self):
        if os.path.isfile(self.error_file):
            os.remove(self.error_file)
        for uid in self.errors:
            self.parse_error(self.errors[uid])

    def parse_error(self, error):
        with open(self.error_file, "a") as file:
            json.dump(error.__dict__, file, indent=4)

    """
    not working
    """

    def check_whitelist(self):
        with open(self.whitelist_file, "r") as file:
            whitelist = json.load(file)
        for whitelist_error in whitelist:
            for uid in self.errors.keys():
                # if whitelist_error.__eq__(errors[uid]):
                self.errors.pop(uid)

    """
    not working
    """

    def add_to_whitelist(self, uid):
        if uid not in self.errors.keys():
            raise  # exception

        # write in whitelist
        with open(self.whitelist_file, "a") as file:
            json.dump(self.errors[uid], file)

        self.errors.pop(uid)

    def run_tools(self):
        chktex.run(self, self.file_to_check)
        detexed_file = tools.detex(self.file_to_check)
        aspell.run(self, detexed_file)
        os.remove(detexed_file)

    def get_lang(self):
        return self.lang


if __name__ == "__main__":
    buddy = LatexBuddy('en')
    buddy.run_tools()
    buddy.parse_to_json()
