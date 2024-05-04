import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import DefaultDict, List
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException

from back.model.airflow import (
    AirflowDagCommandRequest,
    AirflowDagCommandSchema,
    AirflowDagRunResponse,
    AirflowDagRunsResponse,
)
from back.settings import setting
from lib.zetsubou.exceptions import (
    AirflowConflictInArgumentsException,
    AirflowDagIDNotFoundException,
)

APP_TITLE = setting.app_title.lower()
AIRFLOW_HOST = setting.airflow_host
AIRFLOW_USERNAME = setting.airflow_username
AIRFLOW_PASSWORD = setting.airflow_password
AUTH = (AIRFLOW_USERNAME, AIRFLOW_PASSWORD)

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

dags: DefaultDict[str, AirflowDagCommandSchema] = defaultdict(lambda: None)


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

        url = urljoin(self.host, "/api/v1/dags/~/dagRuns/list")
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, auth=self.auth, data=data)
        return AirflowDagRunsResponse(**resp.json())


def is_dag_id(dag_id: str):
    if dags[dag_id] is None:
        raise AirflowDagIDNotFoundException(dag_id)


def get_args(dag_id: str, command_request: AirflowDagCommandRequest, dags=dags) -> str:
    args = ""
    schema: AirflowDagCommandSchema = dags.get(dag_id, None)
    if schema is None:
        raise AirflowDagIDNotFoundException(dag_id)

    schema_kwarg_names = set()
    schema_kwarg_keys = set()
    bool_param_decl_table = {}
    for kwarg in schema.kwargs:
        schema_kwarg_names.add(kwarg.name)
        if len(kwarg.param_decls) == 0:
            continue

        if kwarg.type == "boolean":
            bool_param_decl_table[kwarg.name] = {}
            params = kwarg.param_decls[0].split("/")
            bool_param_decl_table[kwarg.name][True] = params[0]
            if len(params) > 1:
                bool_param_decl_table[kwarg.name][False] = params[1]
            else:
                bool_param_decl_table[kwarg.name][False] = ""

        for param_decl in kwarg.param_decls:
            param_decls = param_decl.split("/")
            for p in param_decls:
                schema_kwarg_keys.add(p)

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
                raise AirflowConflictInArgumentsException
            if kwarg.type == "string" or kwarg.type == "number":
                _kwargs.append(f"--{kwarg.name} {kwarg.value}")
            elif kwarg.type == "boolean":
                is_param_decl = bool_param_decl_table.get(kwarg.name, None)
                if is_param_decl is None:
                    if kwarg.value:
                        _kwargs.append(f"--{kwarg.name}")
                    else:
                        _kwargs.append(f"--no-{kwarg.name}")
                else:
                    _kwarg = bool_param_decl_table.get(kwarg.name, {}).get(
                        kwarg.value, None
                    )
                    if _kwarg is not None or _kwarg != "":
                        _kwargs.append(_kwarg)
        else:
            if kwarg.key not in schema_kwarg_keys:
                raise AirflowConflictInArgumentsException
            if kwarg.type == "string" or kwarg.type == "number":
                _kwargs.append(f"{kwarg.key} {kwarg.value}")
            elif kwarg.type == "boolean":
                _kwargs.append(kwarg.key)

    args = " ".join(_args + _kwargs)

    return args
