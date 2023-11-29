from typing import List, Union

from ...model import (
    TagAttribute,
    TagAttributeCreate,
    TagAttributeCreated,
    TagAttributeUpdate,
)
from ...table import TagAttributeBase
from ..base import (
    count_total,
    create,
    delete_by_id,
    get_row_by,
    get_row_by_id,
    get_rows_order_by_id,
    update_by_id,
)


class CrudTagAttribute(TagAttributeBase):
    @classmethod
    async def create(cls, attr: TagAttributeCreate) -> TagAttributeCreated:
        return TagAttributeCreated(**await create(cls, attr))

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> TagAttribute:
        return await get_row_by_id(cls, id, TagAttribute)

    @classmethod
    async def get_row_by_name(cls, name: str) -> TagAttribute:
        return await get_row_by(cls, cls.name == name, TagAttribute)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagAttribute]:
        return await get_rows_order_by_id(
            cls, TagAttribute, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def update_by_id(cls, attr: TagAttributeUpdate) -> bool:
        return await update_by_id(cls, attr)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
