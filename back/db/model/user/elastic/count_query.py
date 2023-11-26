from pydantic import BaseModel

from back.utils.model import DatetimeStr, JsonStr


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
