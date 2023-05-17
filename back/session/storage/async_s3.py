import io
import json
from pathlib import Path
from typing import List

from aiobotocore.session import AioSession, ClientCreatorContext
from back.model.base import SourceBaseModel
from back.model.s3 import (
    S3DeleteObjectResponse,
    S3DeleteObjectsResponse,
    S3GetObjectResponse,
    S3GetPaginatorResponse,
    S3Object,
    S3PutObjectResponse,
)
from back.settings import setting

AWS_ACCESS_KEY_ID = setting.s3_aws_access_key_id
AWS_SECRET_ACCESS_KEY = setting.s3_aws_secret_access_key
ENDPOINT_URL = setting.s3_endpoint_url


async def generate_presigned_url(
    client, bucket_name: str, object_name: str, expires_in: int = 3600
) -> str:
    resp = await client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_name,
        },
        ExpiresIn=expires_in,
    )
    return resp


async def list_all(client, bucket_name: str, prefix: str) -> List[S3Object]:
    prefixes = []

    paginator = client.get_paginator("list_objects_v2")
    async for page in paginator.paginate(
        Bucket=bucket_name, Prefix=prefix, Delimiter="/"
    ):
        _page = S3GetPaginatorResponse(**page)
        for c in _page.Contents:
            prefixes.append(S3Object(bucket_name=_page.Name, prefix=c.Key))
        for p in _page.CommonPrefixes:
            prefixes.append(S3Object(bucket_name=_page.Name, prefix=p.Prefix))
    return prefixes


async def list_filenames(client, bucket_name: str, prefix: str) -> List[str]:
    _predix = prefix
    if not prefix.endswith("/"):
        _predix += "/"

    filenames = []

    paginator = client.get_paginator("list_objects_v2")
    async for page in paginator.paginate(
        Bucket=bucket_name, Prefix=_predix, Delimiter="/"
    ):
        _page = S3GetPaginatorResponse(**page)
        for c in _page.Contents:
            p = c.Key
            filenames.append(Path(p).name)

    return filenames


async def list_prefixes(client, bucket_name: str, prefix: str) -> List[S3Object]:
    prefixes = []

    paginator = client.get_paginator("list_objects_v2")
    async for page in paginator.paginate(
        Bucket=bucket_name, Prefix=prefix, Delimiter="/"
    ):
        _page = S3GetPaginatorResponse(**page)
        for p in _page.CommonPrefixes:
            prefixes.append(S3Object(bucket_name=_page.Name, prefix=p.Prefix))
    return prefixes


async def list_objects_v2(
    client,
    bucket_name: str,
    prefix: str,
    Delimiter: str = "/",
    MaxKeys: int = 1000,
) -> S3GetPaginatorResponse:

    resp = await client.list_objects_v2(
        Bucket=bucket_name, Prefix=prefix, Delimiter=Delimiter, MaxKeys=MaxKeys
    )
    return S3GetPaginatorResponse(**resp)


async def iter(client, bucket_name: str, prefix: str, depth: int):
    if len(prefix) > 0 and prefix[-1] != "/":
        yield None
    depth -= 1
    objs = await list_prefixes(client, bucket_name, prefix)
    for obj in objs:
        if obj.bucket_name == bucket_name and obj.prefix == prefix:
            continue
        if depth == 0:
            yield obj
        else:
            async for obj in iter(client, bucket_name, obj.prefix, depth):
                yield obj
    yield None


async def exists(client, bucket_name: str, object_name: str) -> bool:
    try:
        await client.head_object(
            Bucket=bucket_name,
            Key=object_name,
        )
        return True
    except client.exceptions.ClientError as e:
        object_name_with_delimiter = object_name
        if not object_name.endswith("/"):
            object_name_with_delimiter = object_name + "/"

        resp = await client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=object_name_with_delimiter,
            Delimiter="/",
            MaxKeys=1,
        )
        prefixes = S3GetPaginatorResponse(**resp)
        if prefixes.KeyCount > 0:
            return True

        # TODO:
        if e.response["Error"]["Code"] == "404":
            ...
        elif e.response["Error"]["Code"] == "403":
            ...
        else:
            raise e

    return False


async def get_object(client, bucket_name: str, object_name: str) -> bytes:
    try:
        _resp = await client.get_object(
            Bucket=bucket_name,
            Key=object_name,
        )
        resp = S3GetObjectResponse(**_resp)
        return await resp.Body.read()
    except client.exceptions.NoSuchKey:
        return None


async def put_object(
    client,
    bucket_name: str,
    object_name: str,
    body: bytes,
    content_type: str = None,
) -> S3PutObjectResponse:
    resp = await client.put_object(
        Bucket=bucket_name, Key=object_name, Body=body, ContentType=content_type
    )
    return S3PutObjectResponse(**resp)


async def put_json(
    client,
    bucket_name: str,
    object_name: str,
    data: dict,
    indent=4,
    ensure_ascii=False,
    encoding: str = "utf-8",
) -> S3PutObjectResponse:
    data_obj = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii).encode(
        encoding=encoding
    )
    data_bytes = io.BytesIO(data_obj)
    return await put_object(
        client, bucket_name, object_name, data_bytes, content_type="application/json"
    )


async def delete_object(client, bucket_name: str, object_name: str) -> bool:
    resp = await client.delete_object(Bucket=bucket_name, Key=object_name)
    resp_obj = S3DeleteObjectResponse(**resp)
    if resp_obj.ResponseMetadata.HTTPStatusCode != 204:
        print(resp)
    if await exists(client, bucket_name, object_name):
        return False
    return True


async def delete(client, bucket_name: str, prefix: str) -> bool:
    _prefix = prefix

    if not await exists(client, bucket_name, _prefix):
        print(f"bucket name: {bucket_name} prefix: {_prefix} did not exist")  # TODO:
        return True

    if not _prefix.endswith("/"):
        if not await delete_object(client, bucket_name, _prefix):
            _prefix += "/"

    objects = []

    paginator = client.get_paginator("list_objects_v2")
    async for page in paginator.paginate(
        Bucket=bucket_name, Prefix=_prefix, Delimiter="/"
    ):
        _page = S3GetPaginatorResponse(**page)

        for c in _page.Contents:
            objects.append({"Key": c.Key})

        for p in _page.CommonPrefixes:
            await delete(client, bucket_name, p.Prefix)

        resp = await client.delete_objects(
            Bucket=bucket_name, Delete={"Objects": objects}
        )

        resp_obj = S3DeleteObjectsResponse(**resp)

        for error in resp_obj.Errors:
            # TODO: raise error?
            print(error)

        objects = []

    return await delete_object(client, bucket_name, _prefix)


class AsyncS3Session(AioSession):
    def __init__(
        self,
        session_vars=None,
        event_hooks=None,
        include_builtin_handlers=True,
        profile=None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        endpoint_url: str = None,
        region_name: str = None,
        is_from_setting_if_none: bool = False,
    ):
        super().__init__(session_vars, event_hooks, include_builtin_handlers, profile)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name

        if is_from_setting_if_none:
            if self.aws_access_key_id is None:
                self.aws_access_key_id = AWS_ACCESS_KEY_ID
            if self.aws_secret_access_key is None:
                self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            if self.endpoint_url is None:
                self.endpoint_url = ENDPOINT_URL

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def create_s3_client(self):
        return ClientCreatorContext(
            self._create_client(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
            )
        )

    async def open(self):
        self.client = await self.create_s3_client().__aenter__()
        return self.client

    async def close(self):
        await self.client.close()

    def get_joined_source(
        self, base_source: SourceBaseModel, relative_path: str
    ) -> SourceBaseModel:
        _base_path = base_source.path
        _relative_path = relative_path
        if not _base_path.endswith("/"):
            _base_path += "/"
        if _relative_path.startswith("/"):
            _relative_path = _relative_path[1:]
        return SourceBaseModel(path=_base_path + "/" + _relative_path)

    async def get_url(self, source: SourceBaseModel) -> str:
        return await generate_presigned_url(
            self.client, source.bucket_name, source.object_name
        )

    async def get_object(self, source: SourceBaseModel) -> bytes:
        return await get_object(self.client, source.bucket_name, source.object_name)

    async def list_filenames(self, source: SourceBaseModel) -> List[str]:
        return await list_filenames(self.client, source.bucket_name, source.object_name)

    async def iter(self, source: SourceBaseModel, depth: int):
        async for obj in iter(
            self.client, source.bucket_name, source.object_name, depth
        ):
            if obj is not None:
                obj_path = f"{source.protocol}-{source.storage_minio_id}://{source.bucket_name}/{obj.prefix}"  # noqa
                obj_source = SourceBaseModel(path=obj_path)
                yield obj_source

    async def exists(self, source: SourceBaseModel) -> bool:
        return await exists(self.client, source.bucket_name, source.object_name)

    async def put_object(
        self, source: SourceBaseModel, body: bytes, content_type: str = None
    ):
        await put_object(
            self.client,
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
            self.client,
            source.bucket_name,
            source.object_name,
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            encoding=encoding,
        )

    async def delete(self, source: SourceBaseModel) -> bool:
        return await delete(self.client, source.bucket_name, source.object_name)
