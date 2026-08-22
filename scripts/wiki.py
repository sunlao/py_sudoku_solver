#!/usr/bin/env python3
"""Copy the GitHub wiki into docs/wiki for local repository access."""

import shutil
import subprocess
import tempfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
WIKI_URL = "https://github.com/sunlao/py_sudoku_solver.wiki.git"
WIKI_DOCS = REPOSITORY_ROOT / "docs" / "wiki"


def copy_wiki() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        wiki_checkout = Path(temporary_directory) / "wiki"
        subprocess.run(
            ["git", "clone", "--depth", "1", WIKI_URL, str(wiki_checkout)],
            check=True,
        )
        shutil.rmtree(WIKI_DOCS, ignore_errors=True)
        shutil.copytree(wiki_checkout, WIKI_DOCS, ignore=shutil.ignore_patterns(".git"))

    print(f"Wiki copied to {WIKI_DOCS}")


if __name__ == "__main__":
    copy_wiki()
