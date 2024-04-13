import time
from datetime import datetime

import pytest

from back.utils.dt import (
    get_isoformat_with_timezone,
    get_now,
    is_isoformat_with_timezone,
    iso2datetime,
    second2iso,
)
from tests.general.logger import logger


def test_second2iso():
    t = time.time()
    logger.debug(f"time: {t}")
    date_str = second2iso(t)
    logger.debug(f"date: {date_str}")
    date = iso2datetime(date_str)
    assert type(date) is datetime


def test_iso2datetime():
    dates_1 = [
        "1970-01-01T01:02:03.456789",
        "1970-01-01T01:02:03.456789+00:00",
        "1970-01-01T01:02:03+00:00",
    ]
    for date in dates_1:
        d = iso2datetime(date)
        assert type(d) is datetime

    d_1 = iso2datetime("1970-01-01T01:02:03.456789")
    d_2 = iso2datetime(d_1)
    assert d_1 == d_2

    dates_2 = ["1970-01-01T01:02:03"]
    for date in dates_2:
        with pytest.raises(ValueError):
            iso2datetime(date)


def print_with_timezone(date: str, ans: bool):
    logger.debug(f"date: {date}")
    has_timezone = is_isoformat_with_timezone(date)
    logger.debug(f"has timezone: {has_timezone}")
    assert has_timezone == ans


def test_is_isoformat_with_timezone():
    print_with_timezone("1970-01-01T01:02:03.456789", False)
    print_with_timezone("1970-01-01T01:02:03.456789+00:00", True)
    print_with_timezone("1970-01-01T01:02:03+00:00", True)


def test_get_isoformat_with_timezone():
    date_str_with_timezone = get_isoformat_with_timezone("1970-01-01T01:02:03.456789")
    assert is_isoformat_with_timezone(date_str_with_timezone)


def test_get_now():
    now = get_now()
    assert is_isoformat_with_timezone(now)
