from pydantic import BaseModel

from back.model.string import DatetimeStr, JsonStr


class UserElasticCountQueryCreate(BaseModel):
    user_id: int
    name: str
    query: JsonStr


class UserElasticCountQueryCreated(UserElasticCountQueryCreate):
    id: int


UserElasticCountQueryUpdate = UserElasticCountQueryCreated


class UserElasticCountQuery(UserElasticCountQueryCreated):
    created: DatetimeStr
    modified: DatetimeStr
