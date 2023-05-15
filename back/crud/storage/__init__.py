from back.crud.storage.s3 import CrudAsyncS3
from back.db.crud import CrudMinioStorage
from back.model.base import Protocol, SourceBaseModel
from fastapi import HTTPException


async def get_storage_client_by_source(source: SourceBaseModel):
    if source.protocol == Protocol.MINIO.value:
        storage_minio_id = source.storage_minio_id
        storage_minio = await CrudMinioStorage.get_row_by_id(storage_minio_id)
        if storage_minio is None:
            raise HTTPException(
                status_code=404,
                detail=f"Minio storage id: {storage_minio_id} not found",
            )

        return CrudAsyncS3(
            aws_access_key_id=storage_minio.access_key,
            aws_secret_access_key=storage_minio.secret_key,
            endpoint_url=storage_minio.endpoint,
        )
