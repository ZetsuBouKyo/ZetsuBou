from typing import List

from ...model import (
    MinioStorage,
    MinioStorageCreate,
    MinioStorageCreated,
    MinioStorageUpdate,
)
from ...table import MinioStorageBase
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


class CrudMinioStorage(MinioStorageBase):
    @classmethod
    async def create(cls, directory: MinioStorageCreate) -> MinioStorageCreated:
        return MinioStorageCreated(**await create(cls, directory))

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> MinioStorage:
        return await get_row_by_id(cls, id, MinioStorage)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[MinioStorage]:
        return await get_rows_order_by_id(
            cls, MinioStorage, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def iter_by_category_order_by_id(
        cls, category: int, limit: int = 100, is_desc: bool = False
    ):
        return iter_by_condition_order_by_id(
            cls, cls.category == category, MinioStorage, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def iter_order_by_id(cls, limit: int = 100, is_desc: bool = False):
        return iter_order_by_id(cls, MinioStorage, limit=limit, is_desc=is_desc)

    @classmethod
    async def update_by_id(cls, directory: MinioStorageUpdate) -> bool:
        return await update_by_id(cls, directory)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
