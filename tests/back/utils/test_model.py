import pytest

from back.utils.model import _Str


def test_str():
    with pytest.raises(NotImplementedError):
        _Str._validate("arg 1", "arg 2")
