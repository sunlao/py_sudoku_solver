#!/usr/bin/env python3
"""Copy selected files from one directory to another."""

import argparse
import shutil
from pathlib import Path


def copy_files(
    source_dir: Path,
    file_names: tuple[str, ...],
    target_dir: Path,
) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)

    for file_name in file_names:
        source_file = source_dir / file_name
        if not source_file.is_file():
            raise FileNotFoundError(source_file)
        shutil.copy2(source_file, target_dir / file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("target_dir", type=Path)
    parser.add_argument("file_names", nargs="+")
    arguments = parser.parse_args()

    copy_files(
        arguments.source_dir,
        tuple(arguments.file_names),
        arguments.target_dir,
    )
