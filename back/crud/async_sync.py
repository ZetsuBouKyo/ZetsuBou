from back.crud.async_gallery import CrudAsyncGallerySync
from back.crud.async_video import CrudAsyncVideoSync
from back.db.crud import CrudStorageMinio
from back.db.model import StorageMinio
from back.model.base import SourceBaseModel, SourceProtocolEnum
from back.model.storage import StorageCategoryEnum
from back.session.storage import get_app_storage_session
from back.session.storage.async_s3 import AsyncS3Session
from fastapi import HTTPException


def get_root_source_by_storage_minio(storage_minio: StorageMinio) -> SourceBaseModel:
    bucket_name = storage_minio.bucket_name
    if bucket_name.endswith("/"):
        bucket_name = bucket_name[:-1]
    prefix = storage_minio.prefix
    if prefix.startswith("/"):
        prefix = prefix[1:]

    root_path = (
        f"{SourceProtocolEnum.MINIO.value}-{storage_minio.id}://{bucket_name}/{prefix}"
    )
    return SourceBaseModel(path=root_path)


async def get_crud_sync(
    protocol: SourceProtocolEnum,
    storage_id: int,
    progress_id: str = None,
    progress_initial: float = 0.0,
    progress_final: float = 100.0,
    is_progress: bool = False,
) -> CrudAsyncGallerySync:
    if protocol == SourceProtocolEnum.MINIO.value:
        storage_minio = await CrudStorageMinio.get_row_by_id(storage_id)
        if storage_minio is None:
            raise HTTPException(
                status_code=404,
                detail=f"Storage MinIO ID: {storage_id} not found",
            )

        if storage_minio.category == StorageCategoryEnum.gallery.value:
            storage_session = AsyncS3Session(
                aws_access_key_id=storage_minio.access_key,
                aws_secret_access_key=storage_minio.secret_key,
                endpoint_url=storage_minio.endpoint,
            )

            root_source = get_root_source_by_storage_minio(storage_minio)

            return CrudAsyncGallerySync(
                storage_session,
                protocol,
                storage_id,
                root_source,
                storage_minio.depth,
                progress_id=progress_id,
                progress_initial=progress_initial,
                progress_final=progress_final,
                is_progress=is_progress,
                is_from_setting_if_none=True,
            )

        elif storage_minio.category == StorageCategoryEnum.video.value:
            app_storage_session = get_app_storage_session(
                protocol, is_from_setting_if_none=True
            )
            storage_session = AsyncS3Session(
                aws_access_key_id=storage_minio.access_key,
                aws_secret_access_key=storage_minio.secret_key,
                endpoint_url=storage_minio.endpoint,
            )

            root_source = get_root_source_by_storage_minio(storage_minio)

            return CrudAsyncVideoSync(
                storage_session,
                protocol,
                storage_id,
                root_source,
                storage_minio.depth,
                app_storage_session=app_storage_session,
                progress_id=progress_id,
                progress_initial=progress_initial,
                progress_final=progress_final,
                is_progress=is_progress,
                is_from_setting_if_none=True,
            )
