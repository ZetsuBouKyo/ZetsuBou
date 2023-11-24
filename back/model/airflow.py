from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class AirflowDagArgumentBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None


class AirflowDagKeywordArgumentBase(BaseModel):
    name: str
    type: Optional[str] = None


class AirflowDagArgument(AirflowDagArgumentBase):
    value: Optional[Any] = None


class AirflowDagKeywordArgument(AirflowDagKeywordArgumentBase):
    key: Optional[str] = None
    value: Optional[Any] = None


class AirflowDagCommandRequest(BaseModel):
    logical_date: Optional[str] = None
    args: List[AirflowDagArgument] = []
    kwargs: List[AirflowDagKeywordArgument] = []


class AirflowDagSchemaArgument(AirflowDagArgumentBase):
    param_decls: List[str] = []
    choices: List[str] = []


class AirflowDagSchemaKeywordArgument(AirflowDagKeywordArgumentBase):
    default: Optional[Any] = None
    param_decls: List[str] = []
    choices: List[str] = []


class AirflowDagCommandSchema(BaseModel):
    dag_id: Optional[str] = None
    sub_command: Optional[str] = None
    doc: Optional[str] = None
    args: List[AirflowDagSchemaArgument] = []
    kwargs: List[AirflowDagSchemaKeywordArgument] = []


class AirflowConf(BaseModel):
    args: str = ""


class AirflowUser(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    roles: List[str]


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
