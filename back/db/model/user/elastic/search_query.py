from pydantic import BaseModel

from back.model.string import DatetimeStr, JsonStr


class UserElasticSearchQueryCreate(BaseModel):
    user_id: int
    name: str
    query: JsonStr


class UserElasticSearchQueryCreated(UserElasticSearchQueryCreate):
    id: int


UserElasticSearchQueryUpdate = UserElasticSearchQueryCreated


class UserElasticSearchQuery(UserElasticSearchQueryCreated):
    created: DatetimeStr
    modified: DatetimeStr
