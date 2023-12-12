from typing import AsyncIterator, List, Optional

from back.model.storage import StorageCategoryEnum

from ...model import (
    StorageMinio,
    StorageMinioCreate,
    StorageMinioCreated,
    StorageMinioUpdate,
)
from ...table import StorageMinioBase
from ..base import (
    count_total,
    create,
    delete_by_id,
    get_row_by_id,
    get_rows_order_by_id,
    iter_by_condition_order_by_id,
    iter_order_by_id,
    update_by_id,
)


class CrudStorageMinio(StorageMinioBase):
    @classmethod
    async def create(cls, directory: StorageMinioCreate) -> StorageMinioCreated:
        category = directory.category
        depth = directory.depth
        if type(category) != int:
            category = category.value

        if category == StorageCategoryEnum.gallery.value:
            assert depth > 0, "depth should greater than 0"
        elif category == StorageCategoryEnum.video.value:
            assert depth == -1, "depth should be -1"

        return StorageMinioCreated(**await create(cls, directory))

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> Optional[StorageMinio]:
        return await get_row_by_id(cls, id, StorageMinio)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[StorageMinio]:
        return await get_rows_order_by_id(
            cls, StorageMinio, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def iter_by_category_order_by_id(
        cls, category: int, limit: int = 100, is_desc: bool = False
    ) -> AsyncIterator[StorageMinio]:
        async for row in iter_by_condition_order_by_id(
            cls, cls.category == category, StorageMinio, limit=limit, is_desc=is_desc
        ):
            yield row

    @classmethod
    async def iter_order_by_id(
        cls, limit: int = 100, is_desc: bool = False
    ) -> AsyncIterator[StorageMinio]:
        async for row in iter_order_by_id(
            cls, StorageMinio, limit=limit, is_desc=is_desc
        ):
            yield row

    @classmethod
    async def update_by_id(cls, directory: StorageMinioUpdate) -> bool:
        return await update_by_id(cls, directory)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
