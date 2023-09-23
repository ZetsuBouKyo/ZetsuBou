import json
from datetime import datetime
from typing import Any, Callable, Union

from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema

from back.utils.dt import datetime_format, datetime_formats


class _Str(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: Callable[[Any], core_schema.JsonSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.general_before_validator_function(
            cls._validate, core_schema.str_schema()
        )

    @classmethod
    def _validate(cls, value: str, _: core_schema.ValidationInfo) -> str:
        raise NotImplementedError


class TagStr(_Str):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> None:
        # json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        # json_schema = handler.resolve_ref_schema(json_schema)
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type="string", format="string")
        return json_schema

    @classmethod
    def _validate(cls, value: str, _: core_schema.ValidationInfo) -> str:
        if value is None:
            return value
        value = str(value)
        if len(value) > 0:
            return value
        raise TypeError(f"length of '{value}' should greater than 0")


class DatetimeStr(_Str):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> None:
        # json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        # json_schema = handler.resolve_ref_schema(json_schema)
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(
            type="string",
            format="datetime",
            examples=["1970-01-01T01:02:03.456789", "1970-01-01T01:02:03.456789+00:00"],
        )
        return json_schema

    @classmethod
    def _validate(
        cls, value: Union[str, datetime], _: core_schema.ValidationInfo
    ) -> str:
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


class JsonStr(_Str):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> None:
        #
        # json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        # json_schema = handler.resolve_ref_schema(json_schema)
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(
            type="string",
            format="json",
        )
        return json_schema

    @classmethod
    def _validate(cls, __input_value: str, _: core_schema.ValidationInfo) -> str:
        if type(__input_value) is str:
            value = json.loads(__input_value)
            value = json.dumps(value)
            return value
        elif type(__input_value) is dict:
            return json.dumps(__input_value)

        raise TypeError("value should be str or json dict")
