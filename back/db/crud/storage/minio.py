from typing import AsyncGenerator, List, Optional

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
    get_all_rows_by_condition_order_by_id,
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

        if category == StorageCategoryEnum.gallery.value:
            assert depth > 0, "depth should greater than 0"
        elif category == StorageCategoryEnum.video.value:
            assert depth == -1, "depth should be -1"

        return StorageMinioCreated(**await create(cls, directory))

    @classmethod
    async def safe_create(cls, directory: StorageMinioCreate) -> StorageMinioCreated:
        existing_storages = await CrudStorageMinio.get_all_rows_by_name_order_by_id(
            directory.name
        )

        field_names = directory.model_fields.keys()
        for existing_storage in existing_storages:
            for field_name in field_names:
                storage_field_value = getattr(directory, field_name, None)
                existing_storage_field_value = getattr(
                    existing_storage, field_name, None
                )
                if storage_field_value != existing_storage_field_value:
                    break
            else:
                return existing_storage
        return await cls.create(directory)

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
    async def get_all_rows_by_name_order_by_id(cls, name: str) -> List[StorageMinio]:
        return await get_all_rows_by_condition_order_by_id(
            cls, cls.name == name, StorageMinio
        )

    @classmethod
    async def iter_by_category_order_by_id(
        cls, category: int, limit: int = 100, is_desc: bool = False
    ) -> AsyncGenerator[StorageMinio]:
        async for row in iter_by_condition_order_by_id(
            cls, cls.category == category, StorageMinio, limit=limit, is_desc=is_desc
        ):
            yield row

    @classmethod
    async def iter_order_by_id(
        cls, limit: int = 100, is_desc: bool = False
    ) -> AsyncGenerator[StorageMinio]:
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
