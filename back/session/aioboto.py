import io
import json
from pathlib import Path
from typing import List

from aiobotocore.session import AioSession, ClientCreatorContext
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


class S3Session(AioSession):
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
    ):
        super().__init__(session_vars, event_hooks, include_builtin_handlers, profile)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name

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


def get_session_from_setting_if_none(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    endpoint_url: str,
    region_name: str,
):
    if aws_access_key_id is None:
        aws_access_key_id = AWS_ACCESS_KEY_ID
    if aws_secret_access_key is None:
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    if endpoint_url is None:
        endpoint_url = ENDPOINT_URL

    return S3Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name=region_name,
    )


async def generate_presigned_url(
    session: S3Session, bucket_name: str, object_name: str, expires_in: int = 3600
) -> str:
    async with session.create_s3_client() as client:
        resp = await client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
            },
            ExpiresIn=expires_in,
        )
        return resp


async def list_all(session: S3Session, bucket_name: str, prefix: str) -> List[S3Object]:
    prefixes = []
    async with session.create_s3_client() as client:
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


async def list_filenames(
    session: S3Session, bucket_name: str, prefix: str
) -> List[str]:
    _predix = prefix
    if not prefix.endswith("/"):
        _predix += "/"

    filenames = []
    async with session.create_s3_client() as client:
        paginator = client.get_paginator("list_objects_v2")
        async for page in paginator.paginate(
            Bucket=bucket_name, Prefix=_predix, Delimiter="/"
        ):
            _page = S3GetPaginatorResponse(**page)
            for c in _page.Contents:
                p = c.Key
                filenames.append(Path(p).name)

    return filenames


async def list_prefixes(
    session: S3Session, bucket_name: str, prefix: str
) -> List[S3Object]:
    prefixes = []
    async with session.create_s3_client() as client:
        paginator = client.get_paginator("list_objects_v2")
        async for page in paginator.paginate(
            Bucket=bucket_name, Prefix=prefix, Delimiter="/"
        ):
            _page = S3GetPaginatorResponse(**page)
            for p in _page.CommonPrefixes:
                prefixes.append(S3Object(bucket_name=_page.Name, prefix=p.Prefix))
    return prefixes


async def list_objects_v2(
    session: S3Session,
    bucket_name: str,
    prefix: str,
    Delimiter: str = "/",
    MaxKeys: int = 1000,
) -> S3GetPaginatorResponse:
    async with session.create_s3_client() as client:
        resp = await client.list_objects_v2(
            Bucket=bucket_name, Prefix=prefix, Delimiter=Delimiter, MaxKeys=MaxKeys
        )
        return S3GetPaginatorResponse(**resp)


async def iter(session: S3Session, bucket_name: str, prefix: str, depth: int):
    if len(prefix) > 0 and prefix[-1] != "/":
        yield None
    depth -= 1
    objs = await list_prefixes(session, bucket_name, prefix)
    for obj in objs:
        if obj.bucket_name == bucket_name and obj.prefix == prefix:
            continue
        if depth == 0:
            yield obj
        else:
            async for obj in iter(session, bucket_name, obj.prefix, depth):
                yield obj
    yield None


async def exists(session: S3Session, bucket_name: str, object_name: str) -> bool:
    async with session.create_s3_client() as client:
        try:
            await client.get_object(
                Bucket=bucket_name,
                Key=object_name,
            )
            return True
        except client.exceptions.NoSuchKey:
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
    return False


async def get_object(session: S3Session, bucket_name: str, object_name: str) -> bytes:
    async with session.create_s3_client() as client:
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
    session: S3Session,
    bucket_name: str,
    object_name: str,
    body: bytes,
    content_type: str = None,
) -> S3PutObjectResponse:
    async with session.create_s3_client() as client:
        resp = await client.put_object(
            Bucket=bucket_name, Key=object_name, Body=body, ContentType=content_type
        )
        return S3PutObjectResponse(**resp)


async def put_json(
    session: S3Session,
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
        session, bucket_name, object_name, data_bytes, content_type="application/json"
    )


async def delete_object(session: S3Session, bucket_name: str, object_name: str) -> bool:
    async with session.create_s3_client() as client:
        resp = await client.delete_object(Bucket=bucket_name, Key=object_name)
        resp_obj = S3DeleteObjectResponse(**resp)
        if resp_obj.ResponseMetadata.HTTPStatusCode != 204:
            print(resp)
    if await exists(session, bucket_name, object_name):
        return False
    return True


async def delete(session: S3Session, bucket_name: str, prefix: str) -> bool:
    _prefix = prefix

    if not await exists(session, bucket_name, _prefix):
        print(f"bucket name: {bucket_name} prefix: {_prefix} did not exist")  # TODO:
        return True

    if not _prefix.endswith("/"):
        if not await delete_object(session, bucket_name, _prefix):
            _prefix += "/"

    objects = []
    async with session.create_s3_client() as client:
        paginator = client.get_paginator("list_objects_v2")
        async for page in paginator.paginate(
            Bucket=bucket_name, Prefix=_prefix, Delimiter="/"
        ):
            _page = S3GetPaginatorResponse(**page)

            for c in _page.Contents:
                objects.append({"Key": c.Key})

            for p in _page.CommonPrefixes:
                await delete(session, bucket_name, p.Prefix)

            resp = await client.delete_objects(
                Bucket=bucket_name, Delete={"Objects": objects}
            )

            resp_obj = S3DeleteObjectsResponse(**resp)

            for error in resp_obj.Errors:
                # TODO: raise error?
                print(error)

            objects = []

    return await delete_object(session, bucket_name, _prefix)
