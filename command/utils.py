import asyncio
from pathlib import Path
from typing import Union

loop = asyncio.get_event_loop()


def sync(func):
    def wrap(*args, **kwargs):
        return loop.run_until_complete(func(*args, **kwargs))

    return wrap


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
