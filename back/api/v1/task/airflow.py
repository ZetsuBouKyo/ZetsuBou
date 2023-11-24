from typing import List

from fastapi import APIRouter, Depends, HTTPException

from back.crud.async_progress import check_airflow_progress
from back.dependency.security import api_security
from back.model.airflow import (
    AirflowDagCommandRequest,
    AirflowDagCommandSchema,
    AirflowDagRunResponse,
    AirflowDagRunsResponse,
)
from back.model.scope import ScopeEnum
from back.model.task import ZetsuBouTask
from back.session.async_airflow import AsyncAirflowSession, dags, get_args, is_dag_id
from back.session.async_redis import async_redis

router = APIRouter(
    prefix="/cmd",
    tags=["Task"],
    dependencies=[api_security([ScopeEnum.task_cmd.value])],
)


def is_progress_id(progress_id: str):
    if not check_airflow_progress(progress_id):
        raise HTTPException(status_code=401, detail="Not authenticated")


@router.get("", response_model=List[AirflowDagCommandSchema])
def get_dags() -> List[AirflowDagCommandSchema]:
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


@router.post(
    "/run/{dag_id}",
    response_model=AirflowDagRunResponse,
    dependencies=[Depends(is_dag_id)],
)
async def trigger_dag_run(
    dag_id: str, command_request: AirflowDagCommandRequest = None
) -> AirflowDagRunResponse:
    conf = {}
    conf["args"] = get_args(dag_id, command_request)
    session = AsyncAirflowSession(is_from_setting_if_none=True)
    return await session.trigger_new_dag_run(
        dag_id, logical_date=command_request.logical_date, conf=conf
    )


@router.get(
    "/schema/{dag_id}",
    response_model=AirflowDagCommandSchema,
    dependencies=[Depends(is_dag_id)],
)
def get_schema(dag_id: str) -> AirflowDagCommandSchema:
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
