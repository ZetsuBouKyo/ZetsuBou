from typing import Any, List

from pydantic import BaseModel


class ArgumentBase(BaseModel):
    name: str = None
    type: str = None


class KeywordArgumentBase(BaseModel):
    name: str
    type: str = None


class Argument(ArgumentBase):
    value: Any = None


class KeywordArgument(KeywordArgumentBase):
    key: str = None
    value: Any = None


class CommandRequest(BaseModel):
    logical_date: str = None
    args: List[Argument] = []
    kwargs: List[KeywordArgument] = []


class SchemaArgument(ArgumentBase):
    param_decls: List[str] = []
    choices: List[str] = []


class SchemaKeywordArgument(KeywordArgumentBase):
    default: Any = None
    param_decls: List[str] = []
    choices: List[str] = []


class CommandSchema(BaseModel):
    dag_id: str = None
    sub_command: str = None
    doc: str = None
    args: List[SchemaArgument] = []
    kwargs: List[SchemaKeywordArgument] = []


class AirflowConf(BaseModel):
    args: str = ""
