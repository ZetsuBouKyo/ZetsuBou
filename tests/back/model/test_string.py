import pytest
from pydantic import BaseModel, ValidationError

from back.model.string import DatetimeStr, HttpUrlStr, JsonStr, _Str
from back.utils.dt import datetime_formats
from lib.faker import ZetsuBouFaker


class D(BaseModel):
    date: DatetimeStr


class H(BaseModel):
    url: HttpUrlStr


class J(BaseModel):
    json_str: JsonStr


def test_str():
    with pytest.raises(NotImplementedError):
        _Str._validate("arg 1", "arg 2")


def test_datetime_str():
    faker = ZetsuBouFaker()
    for format in datetime_formats:
        date_str = faker.random_datetime_str(datetime_formats=[format])
        D(date=date_str)

    D(date=faker.random_datetime_with_utc())


def test_datetime_str_schema():
    faker = ZetsuBouFaker()
    date_str = faker.random_datetime_str(datetime_formats=[datetime_formats[0]])
    d = D(date=date_str)
    d.model_json_schema()


def test_datetime_str_exception():
    date_str = "1970-01-01T01:02:03"
    with pytest.raises(TypeError):
        D(date=date_str)


def test_json_str():
    data = ["{}", '{"id":1,"name":"test"}', {"id": 1, "name": "test"}]
    for d in data:
        J(json_str=d)


def test_json_str_schema():
    j = J(json_str="{}")
    j.model_json_schema()


def test_json_str_exception():
    with pytest.raises(TypeError):
        J(json_str=1)


def test_http_url_str():
    right_data = ["http://abc", "http://abc/", "http://localhost:3000"]
    for data in right_data:
        H(url=data)

    wrong_data = ["HTTP://abc", "http:abc", "http:/abc", "abb", "abc/", "/abc"]
    for data in wrong_data:
        with pytest.raises(ValidationError):
            H(url=data)


def test_http_url_str_schema():
    h = H(url="http://abc")
    h.model_json_schema()


def test_http_url_str_exception():
    with pytest.raises(TypeError):
        H(url=1)
