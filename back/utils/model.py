import json
from datetime import datetime
from typing import Any, Dict, Union

from back.utils.dt import datetime_format, datetime_formats
from pydantic.typing import AnyCallable, Generator

CallableGenerator = Generator[AnyCallable, None, None]


class Str(str):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type="string", format="string")

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> str:
        if value is None:
            return value
        value = str(value)
        if len(value) > 0:
            return value
        raise TypeError(f"length of '{value}' should greater than 0")


class DatetimeStr(str):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(
            type="string",
            format="datetime",
            examples=["1970-01-01T01:02:03.456789", "1970-01-01T01:02:03.456789+00:00"],
        )

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, datetime]) -> str:
        if type(value) is str:
            for f in datetime_formats:
                try:
                    datetime.strptime(value, f)
                    return value
                except ValueError:
                    pass
        elif type(value) is datetime:
            return value.strftime(datetime_format)

        raise TypeError("value should be str or datetime.datetime")


class JsonStr(str):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(
            type="string",
            format="JSON",
        )

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, dict]) -> str:
        if type(value) is str:
            value = json.loads(value)
            value = json.dumps(value)
            return value
        elif type(value) is dict:
            return json.dumps(value)

        raise TypeError("value should be str or json dict")
