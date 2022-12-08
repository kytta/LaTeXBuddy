"""This module contains code for the command-line interface used to run and manage
LaTeXBuddy."""

import argparse
import logging
import os

from pathlib import Path
from time import perf_counter
from typing import AnyStr

from colorama import Fore

from latexbuddy import __app_name__
from latexbuddy import __logger as root_logger
from latexbuddy import __name__ as name
from latexbuddy import __version__, flask_app
from latexbuddy.buddy import LatexBuddy
from latexbuddy.config_loader import ConfigLoader
from latexbuddy.log import __setup_root_logger
from latexbuddy.module_loader import ModuleLoader
from latexbuddy.tools import (
    get_abs_path,
    get_all_paths_in_document,
    perform_whitelist_operations,
)


parser = argparse.ArgumentParser(
    prog=name, description="The one-stop-shop for LaTeX checking.",
)

mutex_group = parser.add_mutually_exclusive_group()

mutex_group.add_argument(
    "--version", "-V", action="version", version=f"{__app_name__} v{__version__}",
)

mutex_group.add_argument(
    "--wl_add_keys",
    "-ak",
    nargs="+",
    metavar="KEY",
    default=None,
    help="Arguments are valid keys that should be added to whitelist. Ideally"
    " the keys are copied from LaTeXBuddy HTML Output",
)
mutex_group.add_argument(
    "--wl_from_wordlist",
    "-awl",
    metavar=("WORD_LIST", "LANGUAGE"),
    nargs=2,
    default=None,
    help="First argument is a file containing a single word per line, "
    "second argument is the language of the words."
    " The words get parsed to keys and the keys get added to the whitelist as "
    "spelling errors that will be ignored by LaTeXBuddy",
)

mutex_group.add_argument(
    "--flask",
    action="store_true",
    default=False,
    help="This option starts a local webserver to check your documents with a GUI.",
)

# TODO: wait for argparse to support nesting of groups in order to make the whole
#  buddy_group mutually exclusive to -V, -ak and -awl
buddy_group = mutex_group.add_argument_group("buddy arguments")

# nargs="+" marks the beginning of a list
buddy_group.add_argument(
    "file", nargs="+", type=Path, help="File(s) that will be processed.",
)
buddy_group.add_argument(
    "--config",
    "-c",
    type=Path,
    default=Path("config.py"),
    help="Location of the config file.",
)
buddy_group.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    default=False,
    help="Display debug output",
)
buddy_group.add_argument(
    "--language",
    "-l",
    type=str,
    default=None,
    help="Target language of the file.",
)
buddy_group.add_argument(
    "--whitelist",
    "-w",
    type=str,
    default=None,
    help="Location of the whitelist file.",
)
buddy_group.add_argument(
    "--output",
    "-o",
    type=str,
    default=None,
    help="Directory, in which to put the output file.",
)
buddy_group.add_argument(
    "--format",
    "-f",
    type=str,
    choices=["HTML", "html", "JSON", "json", "HTML_FLASK", "html_flask"],
    default=None,
    help="Format of the output file (either HTML or JSON).",
)


module_selection = buddy_group.add_mutually_exclusive_group()
module_selection.add_argument(
    "--enable-modules",
    type=str,
    default=None,
    help="Comma-separated list of module names that should be executed. "
    "(Any other module will be implicitly disabled!)",
)
module_selection.add_argument(
    "--disable-modules",
    type=str,
    default=None,
    help="Comma-separated list of module names that should not be executed."
    "(Every other module will be implicitly enabled!)",
)


def main():
    """Parses CLI arguments and launches the LaTeXBuddy instance."""
    start = perf_counter()

    args = parser.parse_args()

    logger = __setup_logger(args)

    print(f"{Fore.CYAN}{__app_name__}{Fore.RESET} v{__version__}")
    logger.debug(f"Parsed CLI args: {str(args)}")

    if args.wl_add_keys or args.wl_from_wordlist:
        perform_whitelist_operations(args)
        return

    if args.flask:
        __execute_flask_startup(args)
        return

    __execute_latexbuddy_checks(args)

    logger.debug(f"Execution finished in {round(perf_counter() - start, 2)}s")


def __setup_logger(args: argparse.Namespace) -> logging.Logger:

    display_debug = args.verbose or os.environ.get("LATEXBUDDY_DEBUG", False)

    __setup_root_logger(root_logger, logging.DEBUG if display_debug else logging.INFO)
    return root_logger.getChild("cli")


def __execute_flask_startup(args: argparse.Namespace) -> None:
    flask_app.run_server()


def __execute_latexbuddy_checks(args: argparse.Namespace) -> None:

    config_loader = ConfigLoader(args)

    """ For each Tex file transferred, all paths
    are fetched and Latexbuddy is executed """

    buddy = LatexBuddy.instance
    module_loader = ModuleLoader(
        Path(
            config_loader.get_config_option_or_default(
                LatexBuddy, "module_dir", "latexbuddy/modules/", verify_type=AnyStr,
            ),
        ),
    )

    for p in args.file:  # args.file is a list
        p = get_abs_path(p)
        first_path = True
        paths = get_all_paths_in_document(Path(p))

        for path in paths:

            # re-initialize the buddy instance with a new path
            buddy.init(
                config_loader=config_loader,
                module_provider=module_loader,
                file_to_check=path,
                path_list=paths,  # to be used later on in render html
                compile_tex=first_path,
            )
            first_path = False

            buddy.run_tools()
            buddy.check_whitelist()
            buddy.output_file()
