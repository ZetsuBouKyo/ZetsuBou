from typing import Any, List, Optional

from pydantic import BaseModel


class ArgumentBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None


class KeywordArgumentBase(BaseModel):
    name: str
    type: Optional[str] = None


class Argument(ArgumentBase):
    value: Optional[Any] = None


class KeywordArgument(KeywordArgumentBase):
    key: Optional[str] = None
    value: Optional[Any] = None


class CommandRequest(BaseModel):
    logical_date: Optional[str] = None
    args: List[Argument] = []
    kwargs: List[KeywordArgument] = []


class SchemaArgument(ArgumentBase):
    param_decls: List[str] = []
    choices: List[str] = []


class SchemaKeywordArgument(KeywordArgumentBase):
    default: Optional[Any] = None
    param_decls: List[str] = []
    choices: List[str] = []


class CommandSchema(BaseModel):
    dag_id: Optional[str] = None
    sub_command: Optional[str] = None
    doc: Optional[str] = None
    args: List[SchemaArgument] = []
    kwargs: List[SchemaKeywordArgument] = []


class AirflowConf(BaseModel):
    args: str = ""
