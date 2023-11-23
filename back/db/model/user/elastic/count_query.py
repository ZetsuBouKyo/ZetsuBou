from pydantic import BaseModel

from back.utils.model import DatetimeStr, JsonStr


class UserElasticCountQueryCreate(BaseModel):
    user_id: int
    name: str
    query: JsonStr


class UserElasticCountQueryCreated(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr


class UserElasticCountQueryUpdate(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr


class UserElasticCountQuery(BaseModel):
    id: int
    user_id: int
    name: str
    query: JsonStr
    created: DatetimeStr
    modified: DatetimeStr
