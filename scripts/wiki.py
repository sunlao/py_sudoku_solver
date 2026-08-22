#!/usr/bin/env python3
"""Copy a local GitHub wiki checkout into docs/wiki."""

import argparse
import shutil
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
WIKI_DOCS = REPOSITORY_ROOT / "docs" / "wiki"


def copy_wiki(source: Path) -> None:
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise NotADirectoryError(f"Wiki directory does not exist: {source}")

    shutil.copytree(
        source,
        WIKI_DOCS,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git"),
    )
    print(f"Wiki copied from {source} to {WIKI_DOCS}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="path to the local wiki directory")
    arguments = parser.parse_args()
    copy_wiki(arguments.source)
