import shutil
from pathlib import Path


def copy() -> None:
    src = Path("/Users/sunlao93/Documents/Git/SunLao/py_sudoku_solver.wiki")
    files = [
        "1-‐-Actor-Overview.md", 
        "2-‐-Operationalizing-Actors.md", 
        "4-‐-Product-Spec.md",
        "5-‐-AI-Agents-in-Actors.md",
        "Home.md"

    ]
    trg = Path("/Users/sunlao93/Documents/Git/SunLao/py_sudoku_solver/docs/llm_spec")
    for f in files:
        src_path = src / f
        if not src_path.is_file():
            raise FileNotFoundError(src_path)
        shutil.copy2(src_path, trg / f)


if __name__ == "__main__":
    copy()