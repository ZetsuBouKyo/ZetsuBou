from typing import Optional

from pydantic import BaseModel

from back.utils.model import DatetimeStr, JsonStr


class UserElasticSearchQueryCreate(BaseModel):
    user_id: Optional[int] = None
    name: str
    query: JsonStr


class UserElasticSearchQueryCreated(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr


class UserElasticSearchQueryUpdate(BaseModel):
    id: int
    user_id: Optional[int] = None
    name: str
    query: JsonStr


class UserElasticSearchQuery(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr
    created: DatetimeStr
    modified: DatetimeStr
