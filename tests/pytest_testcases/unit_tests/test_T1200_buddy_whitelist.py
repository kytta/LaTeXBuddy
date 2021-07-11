import argparse
import os
import tempfile
from pathlib import Path
from typing import List

import pytest

from latexbuddy.buddy import LatexBuddy
from latexbuddy.config_loader import ConfigLoader
from latexbuddy.module_loader import ModuleProvider
from latexbuddy.modules import Module
from latexbuddy.modules.aspell import Aspell
from latexbuddy.problem import Problem


@pytest.fixture
def script_dir():
    return str(Path(os.path.realpath(__file__)).parents[0])


@pytest.fixture
def temp_dir():
    return tempfile.mkdtemp()


@pytest.fixture
def config_loader(script_dir, temp_dir):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=str)

    return ConfigLoader(parser.parse_args(
        ["--config", script_dir + "/resources/T1200_config.py",
         "--output", temp_dir]
    ))


@pytest.fixture
def config_loader_temp_wl(script_dir, temp_dir):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=str)

    return ConfigLoader(parser.parse_args(
        ["--config", script_dir + "/resources/T1200_config_temp_wl.py",
         "--output", temp_dir]
    ))


class DummyModuleProvider(ModuleProvider):

    def load_selected_modules(self, cfg: ConfigLoader) -> List[Module]:
        return []


def init_buddy(scd, cl):

    file = Path(scd + "/resources/T1200_test_document.tex")

    LatexBuddy.init(
        cl,
        DummyModuleProvider(),
        file,
        [file],
    )


def write_original_to_temp_wl(script_dir: str) -> str:
    wl = open(script_dir + "/resources/T1200_whitelist", "r")
    original_content = wl.readlines()
    wl.close()

    with open(script_dir + "/resources/T1200_whitelist_temp", "w") as f:
        f.writelines(original_content)

    return original_content


def test_unit_buddy_whitelist_check_filter(script_dir, config_loader):

    init_buddy(script_dir, config_loader)

    LatexBuddy.add_error(
        Problem(
            (1, 1),
            "Dongbei",
            Aspell,
            Path("/"),
            key="en_spelling_Dongbei",
        )
    )

    assert len(LatexBuddy.instance.errors) == 1

    LatexBuddy.check_whitelist()

    assert len(LatexBuddy.instance.errors) == 0


def test_unit_buddy_whitelist_check_non_filter(script_dir, config_loader):

    init_buddy(script_dir, config_loader)

    LatexBuddy.add_error(
        Problem(
            (1, 1),
            "Dongbeiii",
            Aspell,
            Path("/"),
            key="en_spelling_Dongbeiii",
        )
    )

    assert len(LatexBuddy.instance.errors) == 1

    LatexBuddy.check_whitelist()

    assert len(LatexBuddy.instance.errors) == 1


def test_unit_buddy_whitelist_add_successful(script_dir, config_loader_temp_wl):

    original_content = write_original_to_temp_wl(script_dir)

    init_buddy(script_dir, config_loader_temp_wl)

    LatexBuddy.add_error(
        Problem(
            (1, 1),
            "Dongbeiii",
            Aspell,
            Path("/"),
            key="en_spelling_Dongbeiii",
        )
    )

    assert len(LatexBuddy.instance.errors) == 1
    uid = list(LatexBuddy.instance.errors.keys())[0]

    LatexBuddy.add_to_whitelist(uid)
    assert len(LatexBuddy.instance.errors) == 0

    with open(script_dir + "/resources/T1200_whitelist_temp", "r") as f:
        modified_content = f.readlines()

    assert len(original_content) + 1 == len(modified_content)
    for line in original_content:
        assert line in modified_content
    assert "en_spelling_Dongbeiii\n" in modified_content

    # clear temporary whitelist file
    with open(script_dir + "/resources/T1200_whitelist_temp", "w") as f:
        pass


def test_unit_buddy_whitelist_add_unsuccessful(script_dir, config_loader_temp_wl):

    original_content = write_original_to_temp_wl(script_dir)

    init_buddy(script_dir, config_loader_temp_wl)

    LatexBuddy.add_error(
        Problem(
            (1, 1),
            "Dongbei",
            Aspell,
            Path("/"),
            key="en_spelling_Dongbei",
        )
    )

    assert len(LatexBuddy.instance.errors) == 1
    uid = list(LatexBuddy.instance.errors.keys())[0]

    LatexBuddy.add_to_whitelist(uid + "nonexistent")

    with open(script_dir + "/resources/T1200_whitelist_temp", "r") as f:
        modified_content = f.readlines()

    assert len(original_content) == len(modified_content)
    for line in original_content:
        assert line in modified_content

    # clear temporary whitelist file
    with open(script_dir + "/resources/T1200_whitelist_temp", "w") as f:
        pass
