from typing import List, Optional

from ....model import (
    UserQuestCategory,
    UserQuestCategoryCreate,
    UserQuestCategoryCreated,
)
from ....table import UserQuestCategoryBase
from ...base import create, get_row_by, get_row_by_id, get_rows_order_by_id


class CrudUserQuestCategory(UserQuestCategoryBase):
    @classmethod
    async def create(
        cls, category: UserQuestCategoryCreate
    ) -> UserQuestCategoryCreated:
        return UserQuestCategoryCreated(**await create(cls, category))

    @classmethod
    async def get_row_by_id(cls, id: int) -> Optional[UserQuestCategory]:
        return await get_row_by_id(cls, id, UserQuestCategory)

    @classmethod
    async def get_row_by_name(cls, name: str) -> Optional[UserQuestCategory]:
        return await get_row_by(cls, cls.name == name, UserQuestCategory)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserQuestCategory]:
        return await get_rows_order_by_id(
            cls, UserQuestCategory, skip=skip, limit=limit, is_desc=is_desc
        )
