from typing import Optional

from pydantic import BaseModel

from back.model.string import DatetimeStr


class UserElasticCountQuestCreate(BaseModel):
    name: str
    user_id: Optional[int] = None
    numerator_id: int
    denominator_id: int


class UserElasticCountQuestCreated(UserElasticCountQuestCreate):
    id: int


UserElasticCountQuestUpdate = UserElasticCountQuestCreated


class UserElasticCountQuest(UserElasticCountQuestCreated):
    created: DatetimeStr
    modified: DatetimeStr
