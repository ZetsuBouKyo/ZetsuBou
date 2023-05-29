from typing import List

from back.db.crud import CrudStorageMinio
from back.db.model import (
    StorageMinio,
    StorageMinioCreate,
    StorageMinioCreated,
    StorageMinioUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum
from back.model.storage import StorageCategoryEnum
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/storage-categories",
    dependencies=[api_security([ScopeEnum.storage_minio_storage_categories_get.name])],
)
def get_storage_categories() -> dict:
    return {e.name: e.value for e in StorageCategoryEnum}


@router.get(
    "/total-storages",
    response_model=int,
    dependencies=[api_security([ScopeEnum.storage_minio_total_storages_get.name])],
)
async def count_total_storages() -> int:
    return await CrudStorageMinio.count_total()


@router.get(
    "/storages",
    response_model=List[StorageMinio],
    dependencies=[api_security([ScopeEnum.storage_minio_storages_get.name])],
)
async def get_storages(
    pagination: Pagination = Depends(get_pagination),
) -> List[StorageMinio]:
    return await CrudStorageMinio.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/storage",
    response_model=StorageMinioCreated,
    dependencies=[api_security([ScopeEnum.storage_minio_storage_post.name])],
)
async def post_storage(directory: StorageMinioCreate) -> StorageMinioCreated:
    return await CrudStorageMinio.create(directory)


@router.put(
    "/storage",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.storage_minio_storage_put.name])],
)
async def put_storage(directory: StorageMinioUpdate) -> bool:
    return await CrudStorageMinio.update_by_id(directory)


@router.delete(
    "/storage/{directory_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.storage_minio_storage_delete.name])],
)
async def delete_directory(directory_id: int) -> bool:
    return await CrudStorageMinio.delete_by_id(directory_id)
