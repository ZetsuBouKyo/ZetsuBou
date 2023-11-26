from enum import Enum

from pydantic import BaseModel


class UserQuestCategoryEnum(str, Enum):
    ELASTIC_COUNT_QUEST: str = "ElasticCountQuest"


class UserQuestCategoryCreate(BaseModel):
    name: str


class UserQuestCategoryCreated(UserQuestCategoryCreate):
    id: int


UserQuestCategory = UserQuestCategoryCreated
