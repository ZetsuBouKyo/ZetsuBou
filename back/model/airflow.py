from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class AirflowDagRunStateEnum(str, Enum):
    QUEUED: str = "queued"
    RUNNING: str = "running"
    SUCCESS: str = "success"
    FAILED: str = "failed"


class AirflowDagRunResponse(BaseModel):
    conf: dict = {}
    dag_id: Optional[str] = None
    dag_run_id: Optional[str] = None
    end_date: Optional[str] = None
    execution_date: Optional[str] = None
    external_trigger: Optional[bool] = None
    logical_date: Optional[str] = None
    start_date: Optional[str] = None
    state: Optional[AirflowDagRunStateEnum] = None


class AirflowDagRunsResponse(BaseModel):
    status: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    dag_runs: List[AirflowDagRunResponse] = []
    total_entries: Optional[int] = None


class AirflowHealthMetadatabase(BaseModel):
    status: Optional[str] = None


class AirflowHealthScheduler(AirflowHealthMetadatabase):
    latest_scheduler_heartbeat: Optional[str] = None


class AirflowHealthResponse(BaseModel):
    metadatabase: AirflowHealthMetadatabase = AirflowHealthMetadatabase()
    scheduler: AirflowHealthScheduler = AirflowHealthScheduler()
