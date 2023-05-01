from typing import List

from back.db.crud import CrudMinioStorage
from back.db.model import (
    MinioStorage,
    MinioStorageCategoryEnum,
    MinioStorageCreate,
    MinioStorageCreated,
    MinioStorageUpdate,
    ScopeEnum,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/storage-categories",
    dependencies=[api_security([ScopeEnum.minio_storage_categories_get.name])],
)
def get_storage_categories() -> dict:
    return {e.name: e.value for e in MinioStorageCategoryEnum}


@router.get(
    "/total-storages",
    response_model=int,
    dependencies=[api_security([ScopeEnum.minio_total_storages_get.name])],
)
async def count_total_storages() -> int:
    return await CrudMinioStorage.count_total()


@router.get(
    "/storages",
    response_model=List[MinioStorage],
    dependencies=[api_security([ScopeEnum.minio_storages_get.name])],
)
async def get_storages(
    pagination: Pagination = Depends(get_pagination),
) -> List[MinioStorage]:
    return await CrudMinioStorage.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/storage",
    response_model=MinioStorageCreated,
    dependencies=[api_security([ScopeEnum.minio_storage_post.name])],
)
async def post_storage(directory: MinioStorageCreate) -> MinioStorageCreated:
    return await CrudMinioStorage.create(directory)


@router.put(
    "/storage",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.minio_storage_put.name])],
)
async def put_storage(directory: MinioStorageUpdate) -> bool:
    return await CrudMinioStorage.update_by_id(directory)


@router.delete(
    "/storage/{directory_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.minio_storage_delete.name])],
)
async def delete_directory(directory_id: int) -> bool:
    return await CrudMinioStorage.delete_by_id(directory_id)
