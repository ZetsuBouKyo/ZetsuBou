import httpx
from back.db.crud import CrudStorageMinio
from back.model.base import SourceBaseModel, SourceProtocolEnum
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from fastapi import HTTPException

STORAGE_PROTOCOL = setting.storage_protocol
STORAGE_S3_ENDPOINT_URL = setting.storage_s3_endpoint_url


async def ping_storage() -> bool:
    if STORAGE_PROTOCOL == SourceProtocolEnum.MINIO.value:
        try:
            async with httpx.AsyncClient() as client:
                await client.get(STORAGE_S3_ENDPOINT_URL)
        except httpx.ConnectError:
            return False
        return True
    return False


async def get_storage_session_by_source(
    source: SourceBaseModel,
) -> AsyncS3Session:
    if source.protocol == SourceProtocolEnum.MINIO.value:
        storage_id = source.storage_id
        storage_minio = await CrudStorageMinio.get_row_by_id(storage_id)
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
    protocol: SourceProtocolEnum = None, is_from_setting_if_none: bool = False, **kwargs
) -> AsyncS3Session:
    if is_from_setting_if_none:
        if protocol is None:
            protocol = STORAGE_PROTOCOL

    if protocol == SourceProtocolEnum.MINIO.value:
        if is_from_setting_if_none:
            return AsyncS3Session(is_from_setting_if_none=True)
        return AsyncS3Session(**kwargs)
