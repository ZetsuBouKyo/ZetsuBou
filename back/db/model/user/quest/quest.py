from pydantic import BaseModel
from pydantic.types import NonNegativeInt

from back.model.string import DatetimeStr


class UserQuestCreate(BaseModel):
    user_id: int
    name: str
    category_id: int
    quest_id: int
    priority: NonNegativeInt


class UserQuestCreated(UserQuestCreate):
    id: int


UserQuestUpdate = UserQuestCreated


class UserQuest(UserQuestUpdate):
    created: DatetimeStr
    modified: DatetimeStr
