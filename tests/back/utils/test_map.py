import pytest

from back.utils.map import OneToOneMap


def test_one_to_one_map():
    data = [
        {"id": 1, "name": "red"},
        {"id": 2, "name": "green"},
        {"id": 3, "name": "blue"},
    ]
    m = OneToOneMap(data, "id", "name")
    assert m.get_key("red") == 1
    assert m.get_value(1) == "red"


def test_one_to_one_map_exceptions():
    data_1 = [
        {"id": 1, "name": "red"},
        {"id": 1, "name": "green"},
    ]
    with pytest.raises(ValueError):
        OneToOneMap(data_1, "id", "name")

    data_2 = [
        {"id": 1, "name": "red"},
        {"id": 2, "name": "red"},
    ]
    with pytest.raises(ValueError):
        OneToOneMap(data_2, "id", "name")
