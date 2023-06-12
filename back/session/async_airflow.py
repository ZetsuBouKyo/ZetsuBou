import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import List
from urllib.parse import urljoin

import httpx
from back.model.airflow import AirflowDagRunResponse, AirflowDagRunsResponse
from back.settings import setting

APP_TITLE = setting.app_title.lower()
AIRFLOW_HOST = setting.airflow_host
AIRFLOW_USERNAME = setting.airflow_username
AIRFLOW_PASSWORD = setting.airflow_password
AUTH = (AIRFLOW_USERNAME, AIRFLOW_PASSWORD)

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

dags = defaultdict(lambda: None)


async def trigger_new_dag_run(
    dag_id: str, logical_date: str = None, conf: dict = {}
) -> AirflowDagRunResponse:
    url = urljoin(AIRFLOW_HOST, f"/api/v1/dags/{dag_id}")
    data = {"is_paused": False}
    data = json.dumps(data)
    async with httpx.AsyncClient() as client:
        resp = await client.patch(url, headers=headers, auth=AUTH, data=data)

    now = datetime.now(timezone.utc).isoformat()
    if logical_date is None:
        logical_date = now
    data = {
        "conf": conf,
        "dag_run_id": f"{APP_TITLE}__{now}",
        "logical_date": logical_date,
    }
    data = json.dumps(data)
    url = urljoin(AIRFLOW_HOST, f"/api/v1/dags/{dag_id}/dagRuns")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, auth=AUTH, data=data)

    return AirflowDagRunResponse(**resp.json())


async def get_dag_run(dag_id: str, dag_run_id: str) -> AirflowDagRunResponse:
    url = urljoin(AIRFLOW_HOST, f"/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, auth=AUTH)
    return AirflowDagRunResponse(**resp.json())


async def get_dag_runs(
    dag_ids: List[str],
    page_offset: int = 0,
    page_limit: int = 100,
    order_by: str = None,
) -> AirflowDagRunsResponse:
    data = {"dag_ids": dag_ids, "page_offset": page_offset, "page_limit": page_limit}
    if order_by is not None:
        data["order_by"] = order_by
    data = json.dumps(data)
    url = urljoin(AIRFLOW_HOST, "/api/v1/dags/~/dagRuns/list")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, auth=AUTH, data=data)
    return AirflowDagRunsResponse(**resp.json())
