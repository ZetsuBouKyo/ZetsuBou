import pytest

from back.utils.url import get_host


def test_get_host():
    data = [
        ("https://example.com/home", "https://example.com"),
        ("http://localhost:3000", "http://localhost:3000"),
        ("http://localhost:3000/home", "http://localhost:3000"),
        ("http://0.0.0.0", "http://0.0.0.0"),
        ("http://0.0.0.0:3000/home", "http://0.0.0.0:3000"),
    ]
    data_with_endslash = [
        ("https://example.com/home", "https://example.com/"),
    ]
    data_with_exception = [
        "https://",
        "example.com",
        "example.com/home",
        "localhost:3000",
    ]

    for d in data:
        assert get_host(d[0]) == d[1]

    for d in data_with_endslash:
        assert get_host(d[0], endswith_slash=True)

    for d in data_with_exception:
        with pytest.raises(ValueError):
            get_host(d)
