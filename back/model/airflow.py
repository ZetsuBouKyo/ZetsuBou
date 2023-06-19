from enum import Enum
from typing import List

from pydantic import BaseModel


class AirflowDagRunStateEnum(str, Enum):
    QUEUED: str = "queued"
    RUNNING: str = "running"
    SUCCESS: str = "success"
    FAILED: str = "failed"


class AirflowDagRunResponse(BaseModel):
    conf: dict = {}
    dag_id: str = None
    dag_run_id: str = None
    end_date: str = None
    execution_date: str = None
    external_trigger: bool = None
    logical_date: str = None
    start_date: str = None
    state: AirflowDagRunStateEnum = None


class AirflowDagRunsResponse(BaseModel):
    status: int = None
    title: str = None
    type: str = None
    dag_runs: List[AirflowDagRunResponse] = []
    total_entries: int = None


class AirflowHealthMetadatabase(BaseModel):
    status: str = None


class AirflowHealthScheduler(AirflowHealthMetadatabase):
    latest_scheduler_heartbeat: str = None


class AirflowHealthResponse(BaseModel):
    metadatabase: AirflowHealthMetadatabase = AirflowHealthMetadatabase()
    scheduler: AirflowHealthScheduler = AirflowHealthScheduler()
