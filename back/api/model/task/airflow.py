from typing import Any, List

from pydantic import BaseModel


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


class CommandRequest(FireCommand):
    logical_date: str = None


class CommandSchema(FireCommand):
    dag_id: str = None
    sub_command: str = None
    doc: str = None


class AirflowConf(BaseModel):
    args: str = ""
