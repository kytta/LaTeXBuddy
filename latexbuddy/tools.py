"""This module contains various utility tools."""

import os
import re
import signal
import subprocess
import sys
import traceback

from argparse import Namespace
from logging import Logger
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from latexbuddy.exceptions import ExecutableNotFoundError
from latexbuddy.log import Loggable
from latexbuddy.messages import not_found, path_not_found
from latexbuddy.problem import Problem, ProblemSeverity


class ToolLogger(Loggable):
    pass


logger = ToolLogger().logger


inc_re = re.compile(r"\\include{(?P<package_name>.*)}")
inp_re = re.compile(r"\\input{(?P<package_name>.*)}")

def execute(*cmd: str, encoding: str = "ISO8859-1") -> str:
    """Executes a terminal command with subprocess.

    See usage example in latexbuddy.aspell.

    :param cmd: command name and arguments
    :param encoding: output encoding
    :return: command output
    """

    command = get_command_string(cmd)

    logger.debug(f"Executing '{command}'")

    error_list = subprocess.Popen(
        [command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    out, err_out = error_list.communicate()
    return out.decode(encoding)


def execute_background(*cmd: str) -> subprocess.Popen:
    """Executes a terminal command in background.

    :param cmd: command name and arguments
    :return: subprocess instance of the executed command
    """
    command = get_command_string(cmd)

    logger.debug(f"Executing '{command}' in the background")

    process = subprocess.Popen(
        [command],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
    )
    return process


def kill_background_process(process: subprocess.Popen):
    """Kills previously opened background process.

    For example, it can accept the return value of execute_background() as argument.

    :param process: subprocess instance of the process
    """
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)


def execute_no_errors(*cmd: str, encoding: str = "ISO8859-1") -> str:
    """Executes a terminal command while suppressing errors.

    :param cmd: command name and arguments
    :param encoding: output encoding
    :return: command output
    """
    command = get_command_string(cmd)

    logger.debug(f"Executing '{command}' (ignoring errors)")

    error_list = subprocess.Popen(
        [command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    out, err_out = error_list.communicate()
    return out.decode(encoding)


def get_command_string(cmd: Tuple[str]) -> str:
    """Constructs a command string from a tuple of arguments.

    :param cmd: tuple of command line arguments
    :return: the command string
    """
    command = ""
    for arg in cmd:
        command += str(arg) + " "
    return command.strip()


def find_executable(
    name: str,
    to_install: Optional[str] = None,
    err_logger: Logger = logger,
    log_errors: bool = True,
) -> str:
    """Finds path to an executable. If the executable can not be located, an error
    message is logged to the specified logger, otherwise the executable's path is logged
    as a debug message.

    This uses 'which', i.e. the executable should at least be in user's $PATH

    :param name: executable name
    :param to_install: correct name of the program or project which the requested
                       executable belongs to (used in log messages)
    :param err_logger: custom logger to be used for logging debug/error messages
    :param log_errors: specifies whether or not this method should log an error message,
                       if the executable can not be located; if this is False, a debug
                       message will be logged instead
    :return: path to the executable
    :raises FileNotFoundError: if the executable couldn't be found
    """

    result = execute("which", name)

    if not result or "not found" in result:

        if log_errors:
            err_logger.error(
                not_found(name, to_install if to_install is not None else name)
            )
        else:
            err_logger.debug(
                f"could not find executable '{name}' "
                f"({to_install if to_install is not None else name}) "
                f"in the system's PATH"
            )

        raise ExecutableNotFoundError(
            f"could not find executable '{name}' in system's PATH"
        )

    else:

        path_str = result.splitlines()[0]
        err_logger.debug(f"Found executable {name} at '{path_str}'.")
        return path_str


location_re = re.compile(r"line (\d+), column (\d+)")


def absolute_to_linecol(text: str, position: int) -> Tuple[int, int, List[int]]:
    """Calculates line and column number for an absolute character position.

    :param text: text of file to find line:col position for
    :param position: absolute 0-based character position
    :return: line number, column number, line offsets
    """
    line_offsets = get_line_offsets(text)
    line = 0  # [0, ...]
    while position >= line_offsets[line]:
        line += 1

    # translate_numbers expects 1-based column number
    # however, line_offsets is 0-based
    column = position - line_offsets[line - 1] + 1

    return line, column, line_offsets


def get_line_offsets(text: str) -> List[int]:
    """Calculates character offsets for each line in the file.

    Indices correspond to the line numbers, but are 0-based. For example, if first
    4 lines contain 100 characters (including line breaks), `result[4]` will be 100.
    `result[0]` = 0.

    This is a port of YaLaFi's get_line_starts() function.

    :param text: contents of file to find offsets for
    :return: list of line offsets with indices representing 0-based line numbers
    """
    lines = text.splitlines(keepends=True)
    offset = 0
    result = []
    for line in lines:
        result.append(offset)
        offset += len(line)
    result.append(offset)  # last line

    return result


def is_binary(file_bytes: bytes) -> bool:
    """Detects whether the bytes of a file contain binary code or not.

    For correct detection, it is recommended, that at least 1024 bytes were read.

    Sources:
      * https://stackoverflow.com/a/7392391/4735420
      * https://github.com/file/file/blob/f2a6e7cb7d/src/encoding.c#L151-L228

    :param file_bytes: bytes of a file
    :return: True, if the file is binary, False otherwise
    """
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})
    return bool(file_bytes.translate(None, textchars))


def execute_no_exceptions(
    function_call: Callable[[], None],
    error_message: str = "An error occurred while executing lambda function",
    traceback_log_level: Optional[str] = None,
) -> None:
    """Calls a function and catches any Exception that is raised during this.

    If an Exception is caught, the function is aborted and the error is logged, but as
    the Exception is caught, the program won't crash.

    :param function_call: function to be executed
    :param error_message: custom error message displayed in the console
    :param traceback_log_level: sets the log_level that is used to log the error
                                traceback. If it is None, no traceback will be logged.
                                Valid values are: "DEBUG", "INFO", "WARNING", "ERROR"
    """

    try:
        function_call()
    except Exception as e:

        logger.error(
            f"{error_message}:\n{e.__class__.__name__}: {getattr(e, 'message', e)}"
        )
        if traceback_log_level is not None:

            stack_trace = traceback.format_exc()

            if traceback_log_level == "DEBUG":
                logger.debug(stack_trace)
            elif traceback_log_level == "INFO":
                logger.info(stack_trace)
            elif traceback_log_level == "WARNING":
                logger.warning(stack_trace)
            elif traceback_log_level == "ERROR":
                logger.error(stack_trace)
            else:
                # use level DEBUG as default, in case of invalid value
                logger.debug(stack_trace)


def get_app_dir() -> Path:
    """Finds the directory for storing application data (mostly logs).

    This is a lightweight port of Click's mononymous function:
    https://github.com/pallets/click/blob/af0af571cbbd921d3974a0ff9cf58a4b26bb852b/src/click/utils.py#L412-L458

    :return: path of the application directory
    """

    from latexbuddy import __app_name__ as proper_name
    from latexbuddy import __name__ as unix_name

    # Windows
    if sys.platform.startswith("win"):
        localappdata = os.environ.get("LOCALAPPDATA")
        if localappdata is not None:
            config_home = Path(localappdata)
        else:
            config_home = Path.home()

        app_dir = config_home / proper_name

    # macOS
    elif sys.platform.startswith("darwin"):
        config_home = Path.home() / "Library" / "Application Support"

        app_dir = config_home / proper_name

    # *nix
    else:
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home is not None:
            config_home = Path(xdg_config_home)
        else:
            config_home = Path.home() / ".config"

        app_dir = config_home / unix_name

    app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir


def get_all_paths_in_document_new(file_path: str):
    unchecked_files = []
    checked_files = []
    problems = []

    unchecked_files.append(file_path)

    while len(unchecked_files) > 0:
        unchecked_file = unchecked_files.pop(0)
        unchecked_path = Path(unchecked_file)
        try:
            lines = unchecked_path.read_text().splitlines(keepends=False)
        except FileNotFoundError:
            logger.error(
                path_not_found("the checking of imports", unchecked_path)
            )

            problems.append(
                Problem(
                    position=None,
                    text=unchecked_file,
                    checker="includes",
                    category="latex",
                    p_type="0",
                    file="TBD",
                    severity=ProblemSeverity.WARNING,
                    description=f"File not found {unchecked_file}.",
                    key="includes" + "_" + unchecked_file,
                )
            )

            continue
        except Exception as e:  # If the file cannot be found it is already removed
            error_message = "Error while searching for files"
            logger.error(
                f"{error_message}:\n{e.__class__.__name__}: {getattr(e, 'message', e)}"
            )
            continue

        for line in lines:
            match_inc = inc_re.match(line)
            match_inp = inp_re.match(line)
            if match_inc:
                match = match_inc.group("package_name")
                if not match in unchecked_files and not match in checked_files:
                    unchecked_files.append(match_inc.group("package_name"))
            if match_inp:
                match = match_inp.group("package_name")
                if not match in unchecked_files and not match in checked_files:
                    unchecked_files.append(match_inp.group("package_name"))

        checked_files.append(unchecked_file)

    return pathify_list(checked_files), problems


def pathify_list(list: List[str]) -> List[Path]:
    return [Path(i) for i in list]


def get_all_paths_in_document(file_path: str):
    """Checks files that are included in a file.

    If the file includes more files, these files will also be checked.

    :param file_path:a string, containing file path
    """
    unchecked_files = []  # Holds all unchecked files
    checked_files = []  # Holds all checked file
    problems = []

    # add all paths to list
    # this is used for the command line input
    unchecked_files.append(file_path)
    parent = str(Path(file_path).parent)
    old_lines = ""  # need access to it in creating errors

    while len(unchecked_files) > 0:
        last_checked = checked_files[-1] if len(checked_files) > 0 else ""
        unchecked_file = unchecked_files.pop(0)
        new_files = []
        path_line = {}
        lines = ""  # might not be reset for new file otherwise

        try:
            lines = unchecked_file.read_text().splitlines(keepends=False)
            old_lines = lines
        except FileNotFoundError:  # the file might not be included in path
            logger.error(
                path_not_found("the checking of imports", Path(unchecked_file))
            )

            # TODO: This wont work -->
            line = path_line[unchecked_file]
            if line.startswith("\\input"):
                checker = "inputs"
            else:
                checker = "includes"

            position = re.search(line, old_lines)
            problems.append(
                Problem(
                    position=(1, 1),
                    text=path_line[unchecked_file],
                    checker=checker,
                    category="latex",
                    p_type="0",
                    file=Path(last_checked),
                    severity=ProblemSeverity.WARNING,
                    description=f"File not found {unchecked_file}.",
                    key=checker + "_" + unchecked_file,
                    length=len(line),
                )
            )
            # TODO: This wont work <--
        except Exception as e:  # If the file cannot be found it is already removed

            error_message = "Error while searching for files"
            logger.error(
                f"{error_message}:\n{e.__class__.__name__}: {getattr(e, 'message', e)}"
            )

        for line in lines:
            # check for include and input statements
            if line.startswith("\\include{") or line.startswith("\\input{"):
                path = line
                begin_of_path: int = path.find("{") + 1
                end_of_path: int = path.find("}")
                path = path[begin_of_path:end_of_path]
                # if missing / at the beginning, add it.
                if path[0] != "/":
                    path = parent + "/" + path
                # if missing .tex, add a problem
                if not path.endswith(".tex"):
                    print("'.tex' is missing. Check: \\include{" + path + "}")
                    continue  # if file ending is not given, ignore file

                path_line[path] = line
                new_files.append(Path(path))  # if something was found, add it to a list

        unchecked_files.extend(new_files)  # add new
        checked_files.append(unchecked_file)
    return checked_files, problems


def perform_whitelist_operations(args: Namespace):
    wl_file = args.whitelist if args.whitelist else Path("whitelist")

    if args.wl_add_keys:
        add_whitelist_console(wl_file, args.wl_add_keys)

    if args.wl_from_wordlist:
        add_whitelist_from_file(
            wl_file, Path(args.wl_from_wordlist[0]), args.wl_from_wordlist[1]
        )


def add_whitelist_console(whitelist_file, to_add):
    """
    Adds a list of keys to the Whitelist.
    Keys should be valid keys, ideally copied from LaTeXBuddy HTML Output.

    :param whitelist_file: Path to whitelist file
    :param to_add: list of keys
    """
    whitelist_entries = whitelist_file.read_text().splitlines()
    with whitelist_file.open("a+") as file:
        for key in to_add:
            if key not in whitelist_entries:
                whitelist_entries.append(key)
                file.write(key)
                file.write("\n")


def add_whitelist_from_file(whitelist_file, file_to_parse, lang):
    """
    Takes in a list of words and creates their respective keys,
    then adds them to whitelist.
    Words in the file_to_parse should all be from the same language.
    Each line represents a single Word.

    :param whitelist_file: Path to whitelist file
    :param file_to_parse: Path to wordlist
    :param lang: language of the words in the wordlist
    """
    lines = file_to_parse.read_text().splitlines(keepends=False)
    # TODO check if whitelist file and file to parse is path
    whitelist_entries = whitelist_file.read_text().splitlines()
    with whitelist_file.open("a+") as file:
        for line in lines:
            if line == "":
                continue
            key = lang + "_spelling_" + line
            if key not in whitelist_entries:
                whitelist_entries.append(key)
                file.write(key)
                file.write("\n")


class classproperty(property):
    """Provides a way to implement a python property with class-level accessibility"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
