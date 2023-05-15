from typing import List

from back.crud.storage.base import CrudAsyncStorageBase
from back.model.base import Protocol, SourceBaseModel
from back.session.aioboto import (
    S3Session,
    delete,
    exists,
    generate_presigned_url,
    get_object,
    get_session_from_setting_if_none,
    list_filenames,
    put_json,
    put_object,
)


class CrudAsyncS3(CrudAsyncStorageBase):
    def __init__(
        self,
        storage_id: int = 0,
        protocol: Protocol = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        endpoint_url: str = None,
        region_name: str = "ap-northeast-1-tpe-1",
        is_from_setting_if_none: bool = False,
    ):
        self.storage_id = storage_id
        self.protocol = protocol

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        if is_from_setting_if_none:
            self.session = get_session_from_setting_if_none(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
            )
        else:
            self.session = S3Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
            )

    async def get_url(self, source: SourceBaseModel) -> str:
        return await generate_presigned_url(
            self.session, source.bucket_name, source.object_name
        )

    async def get_object(self, source: SourceBaseModel) -> bytes:
        return await get_object(self.session, source.bucket_name, source.object_name)

    async def list_filenames(self, source: SourceBaseModel) -> List[str]:
        return await list_filenames(
            self.session, source.bucket_name, source.object_name
        )

    async def exists(self, source: SourceBaseModel) -> bool:
        return await exists(self.session, source.bucket_name, source.object_name)

    async def put_object(
        self, source: SourceBaseModel, body: bytes, content_type: str = None
    ):
        await put_object(
            self.session,
            source.bucket_name,
            source.object_name,
            body=body,
            content_type=content_type,
        )

    async def put_json(
        self,
        source: SourceBaseModel,
        data: dict,
        indent=4,
        ensure_ascii=False,
        encoding: str = "utf-8",
    ):
        await put_json(
            self.session,
            source.bucket_name,
            source.object_name,
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            encoding=encoding,
        )

    async def delete(self, source: SourceBaseModel) -> bool:
        return await delete(self.session, source.bucket_name, source.object_name)
