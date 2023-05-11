from typing import List

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
        return StorageMinioCreated(**await create(cls, directory))

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> StorageMinio:
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
    ):
        return iter_by_condition_order_by_id(
            cls, cls.category == category, StorageMinio, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def iter_order_by_id(cls, limit: int = 100, is_desc: bool = False):
        return iter_order_by_id(cls, StorageMinio, limit=limit, is_desc=is_desc)

    @classmethod
    async def update_by_id(cls, directory: StorageMinioUpdate) -> bool:
        return await update_by_id(cls, directory)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
