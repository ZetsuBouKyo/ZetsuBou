from back.db.crud import CrudMinioStorage  # TODO: refactor
from back.model.base import Protocol, SourceBaseModel
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from fastapi import HTTPException

STORAGE_PROTOCOL = setting.storage_protocol


async def get_storage_session_by_source(
    source: SourceBaseModel,
) -> AsyncS3Session:
    if source.protocol == Protocol.MINIO.value:
        storage_id = source.storage_id
        storage_minio = await CrudMinioStorage.get_row_by_id(storage_id)
        if storage_minio is None:
            raise HTTPException(
                status_code=404,
                detail=f"Minio storage id: {storage_id} not found",
            )

        return AsyncS3Session(
            aws_access_key_id=storage_minio.access_key,
            aws_secret_access_key=storage_minio.secret_key,
            endpoint_url=storage_minio.endpoint,
        )


def get_app_storage_session(
    protocol: Protocol = None, is_from_setting_if_none: bool = False, **kwargs
) -> AsyncS3Session:
    if is_from_setting_if_none:
        if protocol is None:
            protocol = STORAGE_PROTOCOL

    if protocol == Protocol.MINIO.value:
        if is_from_setting_if_none:
            return AsyncS3Session(is_from_setting_if_none=True)
        return AsyncS3Session(**kwargs)
