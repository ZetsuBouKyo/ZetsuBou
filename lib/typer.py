import asyncio
import inspect
import sys
from functools import wraps
from inspect import iscoroutinefunction
from typing import Optional

from fastapi.dependencies.utils import get_typed_signature
from typer import Typer
from typer.models import ArgumentInfo, CommandFunctionType, OptionInfo

from back.api.model.task.airflow import Argument, CommandSchema, KeywordArgument
from back.session.async_airflow import dags


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


def airflow_dag_register(
    f: CommandFunctionType, airflow_dag_id: str, airflow_dag_sub_command: str
):
    if airflow_dag_id is None or airflow_dag_sub_command is None:
        return
    schema = CommandSchema(
        dag_id=airflow_dag_id, sub_command=airflow_dag_sub_command, doc=f.__doc__
    )
    typed_signature = get_typed_signature(f)
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

    dags[airflow_dag_id] = schema


class ZetsuBouTyper(Typer):
    def __init__(
        self, *args, loop_factory: Optional[asyncio.AbstractEventLoop] = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.loop_factory = loop_factory

    def command(
        self,
        *args,
        airflow_dag_id: Optional[str] = None,
        airflow_dag_sub_command: Optional[str] = None,
        **kwargs
    ):
        decorator = super().command(*args, **kwargs)

        def add_runner(f):
            airflow_dag_register(f, airflow_dag_id, airflow_dag_sub_command)

            @wraps(f)
            def runner(*args, **kwargs):
                if sys.version_info >= (3, 11) and self.loop_factory:
                    with asyncio.Runner(loop_factory=self.loop_factory) as runner:
                        runner.run(f(*args, **kwargs))
                else:
                    asyncio.run(f(*args, **kwargs))

            if iscoroutinefunction(f):
                return decorator(runner)
            return decorator(f)

        return add_runner
