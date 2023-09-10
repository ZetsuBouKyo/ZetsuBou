from typing import List

from sqlalchemy import and_
from sqlalchemy.sql import functions as func

from ....model import (
    UserElasticCountQuest,
    UserElasticCountQuestCreate,
    UserElasticCountQuestCreated,
    UserElasticCountQuestUpdate,
)
from ....table import UserElasticCountQuestBase
from ...base import (
    count,
    create,
    delete_by,
    get_row_by,
    get_row_by_id,
    get_rows_by_condition_order_by,
    update_by_id,
)


class CrudUserElasticCountQuest(UserElasticCountQuestBase):
    @classmethod
    async def create(
        cls, quest: UserElasticCountQuestCreate
    ) -> UserElasticCountQuestCreated:
        return UserElasticCountQuestCreated(**await create(cls, quest))

    @classmethod
    async def count_by_user_id(cls, user_id: int) -> int:
        return await count(cls, cls.user_id == user_id)

    @classmethod
    async def get_row_by_id(cls, id: int) -> UserElasticCountQuest:
        return await get_row_by_id(cls, id, UserElasticCountQuest)

    @classmethod
    async def get_row_by_user_id_and_quest_id(
        cls, user_id: int, quest_id: int
    ) -> UserElasticCountQuest:
        return await get_row_by(
            cls, and_(cls.id == quest_id, cls.user_id == user_id), UserElasticCountQuest
        )

    @classmethod
    async def get_rows_by_user_id_order_by_id(
        cls, user_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserElasticCountQuest]:
        return await get_rows_by_condition_order_by(
            cls,
            cls.user_id == user_id,
            cls.id,
            UserElasticCountQuest,
            skip,
            limit,
            is_desc,
        )

    @classmethod
    async def update_by_id(cls, quest: UserElasticCountQuestUpdate):
        quest = quest.model_dump()
        quest["modified"] = func.now()
        return await update_by_id(cls, quest)

    @classmethod
    async def delete_by_id_and_user_id(cls, id: int, user_id: int):
        return await delete_by(cls, and_(cls.id == id, cls.user_id == user_id))
