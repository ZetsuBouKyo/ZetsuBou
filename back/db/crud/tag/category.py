from typing import Optional

from ...model import TagCategory, TagCategoryCreate, TagCategoryCreated
from ...table import TagCategoryBase
from ..base import create, delete_by_id, get_row_by_id


class CrudTagCategory(TagCategoryBase):
    @classmethod
    async def create(cls, category: TagCategoryCreate) -> TagCategoryCreated:
        return TagCategoryCreated(**await create(cls, category))

    @classmethod
    async def get_row_by_id(cls, id: int) -> Optional[TagCategory]:
        return await get_row_by_id(cls, id, TagCategory)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
