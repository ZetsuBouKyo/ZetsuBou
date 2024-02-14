from enum import Enum

import typer
from fastapi.dependencies.utils import get_typed_signature
from pydantic import BaseModel
from typer import Typer

from lib.typer import get_parameter_type

app = Typer()


class IntEnum(int, Enum):
    first: int = 1


class StrEnum(str, Enum):
    s: str = ""


class AnyEnum(Enum):
    a: str = ""
    b: int = 1


class Other(BaseModel):
    a: str = ""


@app.command()
def example(
    string: str = typer.Argument(...),
    number_int: int = typer.Argument(...),
    number_float: float = typer.Argument(...),
    boolean: bool = typer.Argument(...),
    empty=typer.Argument(...),
    enum_int: IntEnum = typer.Argument(...),
    enum_str: StrEnum = typer.Argument(...),
    enum_any: AnyEnum = typer.Argument(...),
    other: Other = typer.Argument(...),
):  # pragma: no cover
    ...


def test_get_parameter_type():
    typed_signature = get_typed_signature(example)
    parameters = [(k, v) for k, v in typed_signature.parameters.items()]
    for name, parameter in parameters:
        parameter_type = get_parameter_type(parameter)

        if name == "string":
            assert parameter_type == "string"
        elif name == "number_int":
            assert parameter_type == "number"
        elif name == "number_float":
            assert parameter_type == "number"
        elif name == "boolean":
            assert parameter_type == "boolean"
        elif name == "empty":
            assert parameter_type == "any"
        elif name == "enum_int":
            assert parameter_type == "number"
        elif name == "enum_str":
            assert parameter_type == "string"
        elif name == "enum_any":
            assert parameter_type == "any"
        elif name == "other":
            assert parameter_type == "Other"
