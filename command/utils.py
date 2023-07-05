import inspect
from asyncio import run
from pathlib import Path
from typing import Any, Callable, Union

from fastapi.dependencies.utils import get_typed_signature
from typer.models import ArgumentInfo, OptionInfo

from back.api.model.task.airflow import Argument, CommandSchema, KeywordArgument
from back.session.async_airflow import dags


def sync(async_func):
    def magic(*args, **kwargs):
        return run(async_func(*args, **kwargs))

    magic.__signature__ = inspect.signature(async_func)
    magic.__name__ = async_func.__name__
    magic.__doc__ = async_func.__doc__

    return magic


def is_empty_dir(path: Union[str, Path]) -> bool:
    if type(path) is str:
        path = Path(path)
    if not path.exists():
        print(f"{path} not found")
        return
    if not path.is_dir():
        print(f"{path} is not folder")
        return False
    subs = [p for p in path.iterdir()]
    if len(subs) > 0:
        print(f"{path} is not empty")
        return False

    return True


def get_parameter_type(parameter: inspect.Parameter):
    parameter_type = parameter.annotation
    if parameter_type is str:
        parameter_type = "string"
    elif parameter_type is int or parameter_type is float:
        parameter_type = "number"
    elif parameter_type is bool:
        parameter_type = "boolean"
    elif parameter_type is inspect._empty:
        parameter_type = "any"
    else:
        parameter_type = str(parameter_type)
    return parameter_type


def airflow_dag_register(dag_id: str, sub_command: str):
    def wrap(endpoint: Callable[..., Any]):
        def second_wrap(*args, **kwargs):
            return endpoint(*args, **kwargs)

        schema = CommandSchema(
            dag_id=dag_id, sub_command=sub_command, doc=endpoint.__doc__
        )
        typed_signature = get_typed_signature(endpoint)
        parameters = [(k, v) for k, v in typed_signature.parameters.items()]
        for name, parameter in parameters:
            parameter_type = get_parameter_type(parameter)

            if isinstance(parameter.default, ArgumentInfo):
                schema.args.append(Argument(name=name, type=parameter_type))
            elif isinstance(parameter.default, OptionInfo):
                name = name.replace("_", "-")
                schema.kwargs.append(
                    KeywordArgument(
                        name=name,
                        type=parameter_type,
                        default=parameter.default.default,
                    )
                )

        dags[dag_id] = schema

        second_wrap.__signature__ = inspect.signature(endpoint)
        second_wrap.__name__ = endpoint.__name__
        second_wrap.__doc__ = endpoint.__doc__
        return second_wrap

    return wrap
