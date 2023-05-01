from typing import List

from sqlalchemy import and_
from sqlalchemy.sql import functions as func

from ....model import UserQuest, UserQuestCreate, UserQuestCreated, UserQuestUpdate
from ....table import UserQuestBase
from ...base import (
    count,
    create,
    delete_by,
    get_rows_by_condition_order_by,
    update_by_id,
)


class CrudUserQuest(UserQuestBase):
    @classmethod
    async def create(cls, quest: UserQuestCreate) -> UserQuestCreated:
        return UserQuestCreated(**await create(cls, quest))

    @classmethod
    async def count_by_user_id(cls, user_id: int) -> int:
        return await count(cls, cls.user_id == user_id)

    @classmethod
    async def get_top_priority(cls, user_id: int) -> List[UserQuest]:
        return await get_rows_by_condition_order_by(
            cls, cls.user_id == user_id, cls.priority, UserQuest, 0, 1, False
        )

    @classmethod
    async def get_rows_by_user_id_order_by_id(
        cls, user_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserQuest]:
        return await get_rows_by_condition_order_by(
            cls, cls.user_id == user_id, cls.id, UserQuest, skip, limit, is_desc
        )

    @classmethod
    async def update_by_id(cls, quest: UserQuestUpdate):
        quest = quest.dict()
        quest["modified"] = func.now()
        return await update_by_id(cls, quest)

    @classmethod
    async def delete_by_id_and_user_id(cls, id: int, user_id: int):
        return await delete_by(cls, and_(cls.id == id, cls.user_id == user_id))
