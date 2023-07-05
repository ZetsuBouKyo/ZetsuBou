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


class AsyncAirflowSession:
    def __init__(
        self,
        host: str = None,
        username: str = None,
        password: str = None,
        dag_run_id_prefix: str = None,
        is_from_setting_if_none: bool = False,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.dag_run_id_prefix = dag_run_id_prefix

        if is_from_setting_if_none:
            if self.host is None:
                self.host = AIRFLOW_HOST
            if self.username is None:
                self.username = AIRFLOW_USERNAME
            if self.password is None:
                self.password = AIRFLOW_PASSWORD
            if self.dag_run_id_prefix is None:
                self.dag_run_id_prefix = APP_TITLE

        self.auth = (self.username, self.password)

    async def trigger_new_dag_run(
        self, dag_id: str, logical_date: str = None, conf: dict = {}
    ) -> AirflowDagRunResponse:
        url = urljoin(self.host, f"/api/v1/dags/{dag_id}")
        data = {"is_paused": False}
        data = json.dumps(data)
        async with httpx.AsyncClient() as client:
            resp = await client.patch(url, headers=headers, auth=self.auth, data=data)

        now = datetime.now(timezone.utc).isoformat()
        if logical_date is None:
            logical_date = now
        data = {
            "conf": conf,
            "dag_run_id": f"{self.dag_run_id_prefix}__{now}",
            "logical_date": logical_date,
        }
        data = json.dumps(data)
        url = urljoin(self.host, f"/api/v1/dags/{dag_id}/dagRuns")
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, auth=self.auth, data=data)

        return AirflowDagRunResponse(**resp.json())

    async def get_dag_run(self, dag_id: str, dag_run_id: str) -> AirflowDagRunResponse:
        url = urljoin(self.host, f"/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, auth=self.auth)
        return AirflowDagRunResponse(**resp.json())

    async def get_dag_runs(
        self,
        dag_ids: List[str],
        page_offset: int = 0,
        page_limit: int = 100,
        order_by: str = None,
    ) -> AirflowDagRunsResponse:
        data = {
            "dag_ids": dag_ids,
            "page_offset": page_offset,
            "page_limit": page_limit,
        }
        if order_by is not None:
            data["order_by"] = order_by
        data = json.dumps(data)
        url = urljoin(self.host, "/api/v1/dags/~/dagRuns/list")
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, auth=self.auth, data=data)
        return AirflowDagRunsResponse(**resp.json())
