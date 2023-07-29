import re
from pathlib import Path
from typing import List


def convert(text) -> int:
    return int(text) if text.isdigit() else text


def alphanum_sorting(text) -> List[int]:
    return [convert(c) for c in re.split("([0-9]+)", text)]


def rm_rf(p: Path):
    for child in p.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            rm_rf(child)
    p.rmdir()
