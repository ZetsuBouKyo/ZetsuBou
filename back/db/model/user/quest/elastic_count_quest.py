from pydantic import BaseModel

from back.utils.model import DatetimeStr


class UserElasticCountQuestCreate(BaseModel):
    name: str
    user_id: int = None
    numerator_id: int
    denominator_id: int


class UserElasticCountQuestCreated(BaseModel):
    id: int
    name: str
    user_id: int
    numerator_id: int
    denominator_id: int


class UserElasticCountQuestUpdate(BaseModel):
    id: int
    name: str
    user_id: int = None
    numerator_id: int
    denominator_id: int


class UserElasticCountQuest(BaseModel):
    id: int
    name: str
    user_id: int
    numerator_id: int
    denominator_id: int
    created: DatetimeStr
    modified: DatetimeStr
