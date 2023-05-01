from back.utils.model import DatetimeStr
from pydantic import BaseModel


class UserQuestCreate(BaseModel):
    user_id: int = None
    name: str
    category_id: int
    quest_id: int
    priority: int


class UserQuestCreated(BaseModel):
    id: int
    user_id: int
    name: str
    category_id: int
    quest_id: int
    priority: int


class UserQuestUpdate(BaseModel):
    id: int
    user_id: int = None
    name: str
    category_id: int
    quest_id: int
    priority: int


class UserQuest(BaseModel):
    id: int
    user_id: int
    name: str
    category_id: int
    quest_id: int
    priority: int
    created: DatetimeStr
    modified: DatetimeStr
