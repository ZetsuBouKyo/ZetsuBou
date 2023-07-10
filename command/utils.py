from pathlib import Path
from typing import Union


def is_empty_dir(path: Union[str, Path]) -> bool:
    if type(path) is str:
        path = Path(path)
    if not path.exists():
        print(f"{path} not found")
        return
    if not path.is_dir():
        print(f"{path} is not folder")
        return False
    subs = [p for p in path.iterdir()]
    if len(subs) > 0:
        print(f"{path} is not empty")
        return False

    return True
