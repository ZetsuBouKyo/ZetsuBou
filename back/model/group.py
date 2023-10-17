from enum import Enum

from back.utils.enum import StrEnumMeta


class BuiltInGroupEnum(str, Enum, metaclass=StrEnumMeta):
    admin: str = "admin"
    guest: str = "guest"
