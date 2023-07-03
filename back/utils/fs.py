from pathlib import Path


def rm_rf(p: Path):
    for child in p.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            rm_rf(child)
    p.rmdir()
