from typing import List

from back.api.model.task.airflow import CommandRequest, CommandSchema
from back.model.airflow import AirflowDagRunResponse, AirflowDagRunsResponse
from back.session.airflow import dags
from back.session.airflow import get_dag_run as _get_dag_run
from back.session.airflow import get_dag_runs, trigger_new_dag_run
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


def is_dag_id(dag_id: str):
    if dags[dag_id] is None:
        raise HTTPException(status_code=404, detail=f"Dag ID: {dag_id} not found")


@router.get("", response_model=List[CommandSchema])
def get_dags() -> List[CommandSchema]:
    return list(dags.values())


@router.post(
    "/run/{dag_id}",
    response_model=AirflowDagRunResponse,
    dependencies=[Depends(is_dag_id)],
)
async def trigger_dag_run(
    dag_id: str, command_request: CommandRequest = None
) -> AirflowDagRunResponse:
    conf = {}
    args = ""
    if command_request is not None:
        _args = [arg.value for arg in command_request.args if arg is not None]
        _kwargs = []
        for kwarg in command_request.kwargs:
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
        dag_id, logical_date=command_request.logical_date, conf=conf
    )


@router.get(
    "/schema/{dag_id}", response_model=CommandSchema, dependencies=[Depends(is_dag_id)]
)
def get_schema(dag_id: str) -> CommandSchema:
    return dags[dag_id]


@router.get("/dag-run/{dag_id}/{dag_run_id}", response_model=AirflowDagRunResponse)
async def get_dag_run(dag_id: str, dag_run_id: str) -> AirflowDagRunResponse:
    return await _get_dag_run(dag_id, dag_run_id)


@router.get("/dag-runs", response_model=AirflowDagRunsResponse)
async def list_dag_runs(
    page_offset: int = 0, page_limit: int = 100, order_by: str = None
) -> AirflowDagRunsResponse:
    return await get_dag_runs(
        list(dags.keys()),
        page_offset=page_offset,
        page_limit=page_limit,
        order_by=order_by,
    )
