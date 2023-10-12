from enum import EnumMeta


class StrEnumMeta(EnumMeta):
    def __contains__(cls: type, member: object) -> bool:
        try:
            return super().__contains__(member)
        except TypeError:
            if type(member) is str:
                return member in cls.__members__.values()
            return False
