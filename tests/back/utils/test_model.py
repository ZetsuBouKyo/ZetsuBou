import pytest
from pydantic import BaseModel, ValidationError

from back.utils.model import HttpUrlStr, _Str


def test_str():
    with pytest.raises(NotImplementedError):
        _Str._validate("arg 1", "arg 2")


def test_http_url_str():
    class A(BaseModel):
        url: HttpUrlStr

    right_data = ["http://abc", "http://abc/", "http://localhost:3000"]
    for data in right_data:
        A(url=data)

    wrong_data = ["HTTP://abc", "http:abc", "http:/abc", "abb", "abc/", "/abc"]
    for data in wrong_data:
        with pytest.raises(ValidationError):
            A(url=data)
