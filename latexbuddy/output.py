from pathlib import Path

from jinja2 import Environment, PackageLoader, Template


env = Environment(loader=PackageLoader("latexbuddy"))

# TEST VARIABLES

tex_file_name = "Angebot.tex"

tex_file_text = """\\chapter{Entwicklungsrichtlinien}

Dieses Kapitel beinhaltet Details zu dem Ablauf der Entwicklung der Software.


\\section{Konfigurationsmanagement}

Dieser Abschnitt befasst sich mit dem Thema Konfigurationsmanagement. Hier werden unter anderem die Entwicklungsrichtlinien, -umgebung und der Release-Ablauf beschrieben.

\\subsection{Source-Code-Repository}\\label{angebot:entwicklungsrichtlinien:scm}

Der Source-Code des Projektes wird in einem Git-Repository auf dem Server vom GITZ\\footnote{\\url{https://git.rz.tu-bs.de/sw-technik-fahrzeuginformatik/sep/sep-2021/ibr_alg_0/latexbuddy}} bereitgestellt und verwaltet.

Im Git-Repository gelten für die von Nutzern erstellten Branches und Commits einige Richtlinien, die weiter beschrieben werden."""

errors_list = [
    {
        "path": "Test.tex.detexed",
        "src": "aspell",
        "error_type": "spelling",
        "error_id": "0",
        "text": "Dieser",
        "start": "0",
        "length": 6,
        "suggestions": [
            "Dowser",
            " Diesel",
            " Dieter",
            " Deicer",
            " Dies",
            " Dosser",
            " Dicier",
            " Dies er",
            " Dies-er",
            " Dreiser",
            " Dowse",
            " Duse",
            " Die's",
            " Does",
            " Dose",
            " Dues",
            " Denser",
            " Desert",
            " Dossier",
            " Dis",
            " Deice",
            " Direr",
            " Deer",
            " Douse",
            " Teaser",
            " Terser",
            " Dieters",
            " Dresser",
            " Di's",
            " Dias",
            " Dice",
            " Ties",
            " Dizzier",
            " Defer",
            " Deter",
            " Dimer",
            " Diner",
            " Diver",
            " Miser",
            " Riser",
            " Wiser",
            " Dis's",
            " Dicey",
            " Taser",
            " Doe's",
            " Due's",
            " Dissed",
            " Deer's",
            " Dee's",
            " Tie's",
            " Dieter's",
        ],
        "warning": False,
        "uid": "Test.tex.detexed\u0000aspell\u0000spelling\u00000\u00000\u00006",
    },
    {
        "path": "Test.tex.detexed",
        "src": "aspell",
        "error_type": "spelling",
        "error_id": "0",
        "text": "Kapitel",
        "start": "7",
        "length": 7,
        "suggestions": ["Capitol", " Capital", " Capitol's"],
        "warning": False,
        "uid": "Test.tex.detexed\u0000aspell\u0000spelling\u00000\u00007\u00007",
    },
    {
        "path": "Test.tex.detexed",
        "src": "aspell",
        "error_type": "spelling",
        "error_id": "0",
        "text": "beinhaltet",
        "start": "15",
        "length": 10,
        "suggestions": [
            "Bernhardt",
            " inhaled",
            " Reinhardt",
            " inhalant",
            " reinflated",
            " belated",
            " benighted",
            " inhalator",
            " annihilated",
            " Bernadette",
            " bingled",
            " Brunhilde",
            " belted",
            " halted",
            " beholder",
            " inflated",
            " inhabited",
            " unsalted",
            " blighted",
            " Reinhold",
            " beholden",
            " Bernhardt's",
            " insulted",
            " benefited",
        ],
        "warning": False,
        "uid": "Test.tex.detexed\u0000aspell\u0000spelling\u00000\u000015\u000010",
    },
    {
        "path": "Test.tex.detexed",
        "src": "aspell",
        "error_type": "spelling",
        "error_id": "0",
        "text": "zu",
        "start": "34",
        "length": 2,
        "suggestions": [
            "Z",
            " z",
            " U",
            " u",
            " xi",
            " X",
            " x",
            " Zn",
            " Zr",
            " Zs",
            " Au",
            " Cu",
            " Du",
            " EU",
            " Eu",
            " GU",
            " Lu",
            " Pu",
            " Ru",
            " Tu",
            " Wu",
            " bu",
            " cu",
            " mu",
            " nu",
            " Ci",
            " Si",
            " Sue",
            " Sui",
            " Xe",
            " Zoe",
            " sue",
            " zoo",
            " S",
            " s",
            " Zzz",
            " sou",
            " xii",
            " Ce",
            " SA",
            " SE",
            " SO",
            " SS",
            " SW",
            " Se",
            " so",
            " Zeus",
            " zip",
            " zit",
            " Sir",
            " US",
            " cir",
            " sir",
            " us",
            " xor",
            " I",
            " Luz",
            " Ur",
            " Uzi",
            " i",
            " uh",
            " AZ",
            " CZ",
            " Hz",
            " NZ",
            " Oz",
            " Zulu",
            " Zuni",
            " dz",
            " oz",
            " zebu",
            " GHz",
            " Gus",
            " Hus",
            " SUV",
            " Sun",
            " XL",
            " XS",
            " Z's",
            " Zen",
            " bus",
            " mus",
            " nus",
            " pus",
            " sub",
            " sum",
            " sun",
            " sup",
            " xv",
            " xx",
            " zac",
            " zap",
            " zed",
            " zen",
            " DUI",
            " Eur",
            " GUI",
            " Guy",
            " Hui",
            " Que",
        ],
        "warning": False,
        "uid": "Test.tex.detexed\u0000aspell\u0000spelling\u00000\u000034\u00002",
    },
    {
        "path": "Test.tex.detexed",
        "src": "aspell",
        "error_type": "spelling",
        "error_id": "0",
        "text": "dem",
        "start": "37",
        "length": 3,
        "suggestions": [
            "Dem",
            " Diem",
            " deem",
            " demo",
            " den",
            " fem",
            " DE",
            " EM",
            " em",
            " dam",
            " dim",
            " Dame",
            " dame",
            " dime",
            " dome",
            " dorm",
            " idem",
            " DEA",
            " Dee",
            " dew",
            " DEC",
            " Dec",
            " Del",
            " REM",
            " deb",
            " def",
            " deg",
            " gem",
            " hem",
            " rem",
            " demur",
            " diam",
            " doom",
            " dumb",
            " team",
            " term",
            " TM",
            " Tm",
            " teem",
            " Tim",
            " Tom",
            " tam",
            " tom",
            " tum",
        ],
        "warning": False,
        "uid": "Test.tex.detexed\u0000aspell\u0000spelling\u00000\u000037\u00003",
    },
    {
        "path": "Test.tex.detexed",
        "src": "aspell",
        "error_type": "spelling",
        "error_id": "0",
        "text": "Ablauf",
        "start": "41",
        "length": 6,
        "suggestions": [
            "Ablate",
            " Ablaze",
            " Ably",
            " Bluff",
            " Abelard",
            " Olaf",
            " Able",
            " Alva",
            " Abler",
            " Aloof",
            " Abel",
            " Abloom",
            " Oblate",
            " Balfour",
            " Ebola",
            " ELF",
            " Elf",
            " Bailiff",
        ],
        "warning": False,
        "uid": "Test.tex.detexed\u0000aspell\u0000spelling\u00000\u000041\u00006",
    },
]


def render_html(file_name, file_text, errors):
    template = env.get_template("result.html")
    result = template.render(file_name=file_name, file_text=file_text, errors=errors)
    (Path.cwd() / "output.html").write_text(result)


if __name__ == "__main__":
    render_html(tex_file_name, tex_file_text, errors_list)
