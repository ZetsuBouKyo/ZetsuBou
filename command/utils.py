import inspect
from asyncio import run
from pathlib import Path
from typing import Union


def sync(async_func):
    def magic(*args, **kwargs):
        return run(async_func(*args, **kwargs))

    magic.__signature__ = inspect.signature(async_func)
    magic.__name__ = async_func.__name__
    magic.__doc__ = async_func.__doc__

    return magic


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
