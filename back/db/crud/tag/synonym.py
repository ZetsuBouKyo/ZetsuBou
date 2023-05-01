from typing import List

from ...model import TagSynonym, TagSynonymCreate, TagSynonymCreated, TagSynonymUpdate
from ...table import TagSynonymBase
from ..base import create, delete_by_id, get_rows_order_by_id, update_by_id


class CrudTagSynonym(TagSynonymBase):
    @classmethod
    async def create(cls, synonym: TagSynonymCreate) -> TagSynonymCreated:
        return TagSynonymCreated(**await create(cls, synonym))

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagSynonym]:
        return await get_rows_order_by_id(
            cls, TagSynonym, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def update_by_id(cls, synonym: TagSynonymUpdate) -> bool:
        return await update_by_id(cls, synonym)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
