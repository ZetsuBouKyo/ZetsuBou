from back.utils.model import DatetimeStr, JsonStr
from pydantic import BaseModel


class UserElasticSearchQueryCreate(BaseModel):
    user_id: int = None
    name: str
    query: JsonStr


class UserElasticSearchQueryCreated(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr


class UserElasticSearchQueryUpdate(BaseModel):
    id: int
    user_id: int = None
    name: str
    query: JsonStr


class UserElasticSearchQuery(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr
    created: DatetimeStr
    modified: DatetimeStr
