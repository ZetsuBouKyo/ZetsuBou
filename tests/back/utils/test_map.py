import pytest

from back.utils.map import BiDict, OneToOneMap


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


def test_bidict_default():
    b = BiDict()
    assert b.get(1) is None
    assert b.get(2) is None
    assert b[3] is None
    assert len(b) == 0


def test_bidict():
    b = BiDict()
    b[1] = "red"
    b["green"] = 2
    b[3] = "blue"

    assert len(b) == 3
    assert b[1] == "red"
    assert b["red"] == 1
    assert b[2] == "green"
    assert b["green"] == 2
    assert b[3] == "blue"
    assert b["blue"] == 3

    b[1] = "white"
    assert len(b) == 3
    assert b[1] == "white"
    assert b["white"] == 1

    b[1] = "white"
    assert len(b) == 3
    assert b[1] == "white"
    assert b["white"] == 1

    b[4] = "white"
    assert len(b) == 3
    assert b[4] == "white"
    assert b["white"] == 4
    assert b[1] is None


def test_bidict_exceptions():
    with pytest.raises(ValueError):
        b = BiDict()
        b[1] = 1

    with pytest.raises(ValueError):
        b = BiDict()
        b[1] = None

    with pytest.raises(ValueError):
        b = BiDict()
        b[None] = 1


def test_bidict_type_hint():
    BiDict[int, str]
