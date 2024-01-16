from datetime import datetime

from back.utils.dt import get_now, iso2datetime


def datetime_validator(table_base, func_name: str) -> bool:
    now_str = get_now()
    now_dt = iso2datetime(now_str)
    base = table_base()
    func = getattr(base, func_name)
    n1 = func(None, now_str)
    n2 = func(None, now_dt)
    return type(n1) is datetime and type(n2) is datetime
