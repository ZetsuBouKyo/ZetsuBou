from typing import List

from fastapi import APIRouter, Depends

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
from back.model.storage import StorageCategoryEnum, StorageStat
from back.session.storage import AsyncS3Session
from back.session.storage.async_s3 import get_source

router = APIRouter(tags=["Minio Storage"])


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


@router.get(
    "/storage/{storage_id}/stat",
    response_model=StorageStat,
    dependencies=[api_security([ScopeEnum.storage_minio_storage_stat_get.name])],
)
async def get_storage_stat(storage_id: int) -> StorageStat:
    storage = await CrudStorageMinio.get_row_by_id(storage_id)
    session = AsyncS3Session(
        aws_access_key_id=storage.access_key,
        aws_secret_access_key=storage.secret_key,
        endpoint_url=storage.endpoint,
    )
    source = get_source(storage.bucket_name, storage.prefix)

    async with session:
        return await session.get_storage_stat(source, storage.depth)


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
