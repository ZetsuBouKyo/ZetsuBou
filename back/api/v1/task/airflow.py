from typing import List

from fastapi import APIRouter, Depends, HTTPException

from back.api.model.task.airflow import CommandRequest, CommandSchema
from back.crud.async_progress import check_airflow_progress
from back.dependency.security import api_security
from back.model.airflow import AirflowDagRunResponse, AirflowDagRunsResponse
from back.model.scope import ScopeEnum
from back.model.task import ZetsuBouTask
from back.session.async_airflow import AsyncAirflowSession, dags
from back.session.async_redis import async_redis

router = APIRouter(
    prefix="/cmd", tags=["Task"], dependencies=[api_security(ScopeEnum.task_cmd.name)]
)


def dag_id_not_found_exception(dag_id):
    return HTTPException(status_code=404, detail=f"Dag ID: {dag_id} not found")


def is_progress_id(progress_id: str):
    if not check_airflow_progress(progress_id):
        raise HTTPException(status_code=401, detail="Not authenticated")


def is_dag_id(dag_id: str):
    if dags[dag_id] is None:
        raise dag_id_not_found_exception(dag_id)


@router.get("", response_model=List[CommandSchema])
def get_dags() -> List[CommandSchema]:
    return list(dags.values())


@router.get(
    "/progress/{progress_id}",
    response_model=ZetsuBouTask,
    dependencies=[Depends(is_progress_id)],
)
async def get_progress(progress_id: str) -> ZetsuBouTask:
    progress = await async_redis.get(progress_id)
    if progress is None:
        return ZetsuBouTask()
    return ZetsuBouTask(progress_id=progress_id, progress=float(progress))


@router.delete(
    "/progress/{progress_id}",
    dependencies=[Depends(is_progress_id)],
)
async def delete_progress(progress_id: str):
    await async_redis.delete(progress_id)


conflict_in_arguments_exception = HTTPException(
    status_code=409,
    detail="Conflict in arguments",
)


def get_args(dag_id: str, command_request: CommandRequest, dags=dags) -> str:
    args = ""
    schema: CommandSchema = dags.get(dag_id, None)
    if schema is None:
        raise dag_id_not_found_exception(dag_id)

    schema_kwarg_names = set()
    schema_kwargs = set()
    for kwarg in schema.kwargs:
        schema_kwarg_names.add(kwarg.name)
        if not kwarg.param_decls:
            continue
        for param_decl in kwarg.param_decls:
            param_decls = param_decl.split("/")
            for p in param_decls:
                schema_kwargs.add(p)

    if command_request is None:
        return args

    if len(schema.args) != len(command_request.args):
        raise HTTPException(
            status_code=409,
            detail="Conflict in arguments",
        )
    _args = [str(arg.value) for arg in command_request.args if arg.value is not None]
    _kwargs = []
    for kwarg in command_request.kwargs:
        if kwarg.value is None:
            continue

        if kwarg.key is None:
            if kwarg.name not in schema_kwarg_names:
                raise conflict_in_arguments_exception
            if kwarg.type == "string" or kwarg.type == "number":
                _kwargs.append(f"--{kwarg.name} {kwarg.value}")
            elif kwarg.type == "boolean":
                if kwarg.value:
                    _kwargs.append(f"--{kwarg.name}")
                else:
                    _kwargs.append(f"--no-{kwarg.name}")
        else:
            if kwarg.key not in schema_kwargs:
                raise conflict_in_arguments_exception
            if kwarg.type == "string" or kwarg.type == "number":
                _kwargs.append(f"--{kwarg.key} {kwarg.value}")
            elif kwarg.type == "boolean":
                _kwargs.append(kwarg.key)

    args = " ".join(_args + _kwargs)

    return args


@router.post(
    "/run/{dag_id}",
    response_model=AirflowDagRunResponse,
    dependencies=[Depends(is_dag_id)],
)
async def trigger_dag_run(
    dag_id: str, command_request: CommandRequest = None
) -> AirflowDagRunResponse:
    conf = {}
    conf["args"] = get_args(dag_id, command_request)
    session = AsyncAirflowSession(is_from_setting_if_none=True)
    return await session.trigger_new_dag_run(
        dag_id, logical_date=command_request.logical_date, conf=conf
    )


@router.get(
    "/schema/{dag_id}", response_model=CommandSchema, dependencies=[Depends(is_dag_id)]
)
def get_schema(dag_id: str) -> CommandSchema:
    return dags[dag_id]


@router.get("/dag-run/{dag_id}/{dag_run_id}", response_model=AirflowDagRunResponse)
async def get_dag_run(dag_id: str, dag_run_id: str) -> AirflowDagRunResponse:
    session = AsyncAirflowSession(is_from_setting_if_none=True)
    return await session.get_dag_run(dag_id, dag_run_id)


@router.get("/dag-runs", response_model=AirflowDagRunsResponse)
async def list_dag_runs(
    page_offset: int = 0, page_limit: int = 100, order_by: str = None
) -> AirflowDagRunsResponse:
    session = AsyncAirflowSession(is_from_setting_if_none=True)
    return await session.get_dag_runs(
        list(dags.keys()),
        page_offset=page_offset,
        page_limit=page_limit,
        order_by=order_by,
    )
