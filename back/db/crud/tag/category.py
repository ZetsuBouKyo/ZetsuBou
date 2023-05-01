from typing import List

from ...model import (
    TagCategory,
    TagCategoryCreate,
    TagCategoryCreated,
    TagCategoryUpdate,
)
from ...table import TagCategoryBase
from ..base import (
    create,
    delete_by_id,
    get_rows_by_condition_order_by_id,
    get_rows_order_by_id,
    update_by_id,
)


class CrudTagCategory(TagCategoryBase):
    @classmethod
    async def create(cls, category: TagCategoryCreate) -> TagCategoryCreated:
        return TagCategoryCreated(**await create(cls, category))

    @classmethod
    async def get_row_by_category_id_and_token_id(
        cls, category_id: int, token_id: int
    ) -> TagCategory:
        # TODO:
        return

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagCategory]:
        return await get_rows_order_by_id(
            cls, TagCategory, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def get_rows_order_by_id_by_category_id(
        cls, category_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagCategory]:
        return await get_rows_by_condition_order_by_id(
            cls,
            cls.linked_id == category_id,
            TagCategory,
            skip=skip,
            limit=limit,
            is_desc=is_desc,
        )

    @classmethod
    async def get_rows_order_by_id_by_token_id(
        cls, token_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagCategory]:
        return await get_rows_by_condition_order_by_id(
            cls,
            cls.token_id == token_id,
            TagCategory,
            skip=skip,
            limit=limit,
            is_desc=is_desc,
        )

    @classmethod
    async def update_by_id(cls, category: TagCategoryUpdate) -> bool:
        return await update_by_id(cls, category)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
