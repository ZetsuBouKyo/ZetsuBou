import inspect
from collections import defaultdict
from typing import Any, Callable, List

from back.model.airflow import AirflowDagRunResponse, AirflowDagRunsResponse
from back.session.airflow import get_dag_runs, trigger_new_dag_run
from fastapi import APIRouter, Depends, HTTPException
from fastapi.dependencies.utils import get_typed_signature
from pydantic import BaseModel
from typer.models import ArgumentInfo, OptionInfo

dags = defaultdict(lambda: None)


def is_dag_id(dag_id: str):
    if dags[dag_id] is None:
        raise HTTPException(status_code=404, detail=f"Dag ID: {dag_id} not found")


router = APIRouter()


class Argument(BaseModel):
    name: str = None
    type: str = None
    value: Any = None


class KeywordArgument(BaseModel):
    name: str
    type: str = None
    default: Any = None
    value: Any = None


class FireCommand(BaseModel):
    args: List[Argument] = []
    kwargs: List[KeywordArgument] = []


class FireCommandRequest(FireCommand):
    logical_date: str = None


class FireCommandSchema(FireCommand):
    dag_id: str = None
    sub_command: str = None
    doc: str = None


class AirflowConf(BaseModel):
    args: str = ""


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


def register(dag_id: str, sub_command: str):
    def wrap(endpoint: Callable[..., Any]):
        def second_wrap(*args, **kwargs):
            return endpoint(*args, **kwargs)

        schema = FireCommandSchema(
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


def get_dags() -> List[FireCommandSchema]:
    return list(dags.values())


async def trigger_dag_run(
    dag_id: str, fire_command: FireCommandRequest = None
) -> AirflowDagRunResponse:
    conf = {}
    args = ""
    if fire_command is not None:
        _args = [arg.value for arg in fire_command.args if arg is not None]
        _kwargs = []
        for kwarg in fire_command.kwargs:
            if kwarg.value is None:
                continue
            if kwarg.type == "string" or kwarg.type == "number":
                _kwargs.append(f"--{kwarg.name} {kwarg.value}")
            elif kwarg.type == "boolean":
                if kwarg.value:
                    _kwargs.append(f"--{kwarg.name}")
                else:
                    _kwargs.append(f"--no-{kwarg.name}")
        args = " ".join(_args + _kwargs)

    conf["args"] = args

    return await trigger_new_dag_run(
        dag_id, logical_date=fire_command.logical_date, conf=conf
    )


def get_schema(dag_id: str) -> FireCommandSchema:
    return dags[dag_id]


async def list_dag_runs(
    page_offset: int = 0, page_limit: int = 100, order_by: str = None
) -> AirflowDagRunsResponse:
    return await get_dag_runs(
        list(dags.keys()),
        page_offset=page_offset,
        page_limit=page_limit,
        order_by=order_by,
    )


router.add_api_route(
    "", get_dags, methods=["GET"], response_model=List[FireCommandSchema]
)
router.add_api_route(
    "/dag-runs", list_dag_runs, methods=["GET"], response_model=AirflowDagRunsResponse
)
router.add_api_route(
    "/run/{dag_id}",
    trigger_dag_run,
    methods=["POST"],
    response_model=AirflowDagRunResponse,
    dependencies=[Depends(is_dag_id)],
)
router.add_api_route(
    "/schema/{dag_id}",
    get_schema,
    methods=["GET"],
    response_model=FireCommandSchema,
    dependencies=[Depends(is_dag_id)],
)
