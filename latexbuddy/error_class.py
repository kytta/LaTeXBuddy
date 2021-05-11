import hashlib

i = "1"
class Error:
    """
    creates an error object
    """

    def __init__(
        self,
        buddy,
        path,           # the path to the file
        src,            # the src tool of the error <chktex/aspell/...>
        error_type,     # <grammar/spelling/latex>
        error_id,       # tool intern error id as integer
        text,           # the error as text if possible
        start,          # the starting character
        length,         # the length
        suggestions,    # suggestions to solve the error
        warning,        # boolean. true if the error is a warning, only in tex checks
        compare_id      # ID to compare two errors that are semantically equal, to be
                        # implemented by each module TODO: make sure all modules do this
    ):
        self.dict = {
            "path": path,
            "src": src,
            "error_type": error_type,
            "error_id": error_id,
            "text": text,
            "start": start,
            "length": length,
            "suggestions": suggestions,
            "warning": warning,
            "uid": self.uid(),
            "compare_id": compare_id
        }
        buddy.add_error(self)

    """
    creates uid
    """

    def uid(self):
        """return "{}\0{}\0{}\0{}\0{}\0{}".format(
            self.dict["path"],
            self.dict["src"],
            self.dict["error_type"],
            self.dict["error_id"],
            self.dict["start"],
            self.dict["length"],
        )"""
        global i
        i = i + "1"
        return i

    """
    gets uid
    """

    def get_uid(self):
        return self.dict["uid"]

    def get_comp_id(self):
        return self.dict["compare_id"]

    # TODO: Ignore for now (maybe different hashes for different error types)
    # def get_hash(self, language):
    #    string_for_hash = self.dict["error_type"] + self.dict["text"] + language
    #    return hashlib.md5(string_for_hash).hexdigest()

    def compare_with_other_comp_id(self, other_comp_id):
        return self.dict["compare_id"] == other_comp_id
