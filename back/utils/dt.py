from datetime import datetime
from typing import List, Union

import pytz
from sqlalchemy.sql.functions import now

from back.settings import setting

TIMEZONE = setting.app_timezone

datetime_format_db = r"%Y-%m-%dT%H:%M:%S.%f"
datetime_format = r"%Y-%m-%dT%H:%M:%S.%f%z"
datetime_format_no_f = r"%Y-%m-%dT%H:%M:%S%z"
datetime_formats = [datetime_format_db, datetime_format, datetime_format_no_f]


def second2iso(time: float) -> str:
    return datetime.fromtimestamp(time).strftime(datetime_format)


def iso2datetime(
    date: Union[str, datetime, now], formats: List[str] = datetime_formats
) -> Union[datetime, now]:
    if type(date) is str:
        for f in formats:
            try:
                return datetime.strptime(date, f)
            except ValueError:
                pass
        raise ValueError(f"time data {date} does not match any format")
    return date


def is_isoformat_with_timezone(date: str) -> str:
    datetime = iso2datetime(date)
    if datetime.tzinfo is None:
        return False
    return True


def get_isoformat_with_timezone(date: str) -> str:
    z = pytz.timezone(TIMEZONE)
    date = iso2datetime(date)
    return z.localize(date).isoformat()


def get_now(tz: str = TIMEZONE) -> str:
    return datetime.now(pytz.timezone(tz)).isoformat()
