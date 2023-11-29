from enum import Enum

from back.utils.enum import StrEnumMeta


class StrEnum(str, Enum, metaclass=StrEnumMeta):
    a: str = "a"
    b: str = "b"


def test():
    s = StrEnum
    for e in s:
        assert e in s
        assert e.value in s

    assert "c" not in s
    assert 1 not in s
