import io
import json
from typing import List

from back.model.s3 import (
    S3DeleteObjectResponse,
    S3DeleteObjectsResponse,
    S3GetPaginatorResponse,
    S3Object,
    S3PutObjectResponse,
)
from back.session.aioboto import S3Session
from back.settings import setting

AWS_ACCESS_KEY_ID = setting.s3_aws_access_key_id
AWS_SECRET_ACCESS_KEY = setting.s3_aws_secret_access_key
ENDPOINT_URL = setting.s3_endpoint_url


class CrudS3:
    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        endpoint_url: str = None,
        region_name: str = "ap-northeast-1-tpe-1",
        is_from_setting_if_none: bool = False,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        if is_from_setting_if_none:
            self.init_from_setting()

        self.session = S3Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
        )

    def init_from_setting(self):
        if self.aws_access_key_id is None:
            self.aws_access_key_id = AWS_ACCESS_KEY_ID
        if self.aws_secret_access_key is None:
            self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        if self.endpoint_url is None:
            self.endpoint_url = ENDPOINT_URL

    async def generate_presigned_url(
        self, bucket_name: str, object_name: str, expires_in: int = 3600
    ) -> str:
        async with self.session.create_s3_client() as client:
            resp = await client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": object_name,
                },
                ExpiresIn=expires_in,
            )
            return resp

    async def list(self, bucket_name: str, prefix: str) -> List[S3Object]:
        prefixes = []
        async with self.session.create_s3_client() as client:
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

    async def list_objects_v2(
        self, bucket_name: str, prefix: str, Delimiter: str = "/", MaxKeys: int = 1000
    ) -> S3GetPaginatorResponse:
        async with self.session.create_s3_client() as client:
            resp = await client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix, Delimiter=Delimiter, MaxKeys=MaxKeys
            )
            return S3GetPaginatorResponse(**resp)

    async def exists(self, bucket_name: str, object_name: str) -> bool:
        async with self.session.create_s3_client() as client:
            try:
                await client.get_object(
                    Bucket=bucket_name,
                    Key=object_name,
                )
                return True
            except client.exceptions.NoSuchKey:
                if not object_name.endswith("/"):
                    object_name = f"{object_name}/"

                resp = await client.list_objects_v2(
                    Bucket=bucket_name, Prefix=object_name, Delimiter="/", MaxKeys=1
                )
                prefixes = S3GetPaginatorResponse(**resp)
                if prefixes.KeyCount > 0:
                    return True
        return False

    async def get_object(self, bucket_name: str, object_name: str):
        async with self.session.create_s3_client() as client:
            resp = await client.get_object(Bucket=bucket_name, Key=object_name)
            print(resp)
            # return S3PutObjectResponse(**resp)

    async def put_object(
        self, bucket_name: str, object_name: str, body: bytes, content_type: str = None
    ) -> S3PutObjectResponse:
        async with self.session.create_s3_client() as client:
            resp = await client.put_object(
                Bucket=bucket_name, Key=object_name, Body=body, ContentType=content_type
            )
            return S3PutObjectResponse(**resp)

    async def put_json(
        self,
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
        return await self.put_object(
            bucket_name, object_name, data_bytes, content_type="application/json"
        )

    async def delete_object(self, bucket_name: str, object_name: str) -> bool:
        async with self.session.create_s3_client() as client:
            resp = await client.delete_object(Bucket=bucket_name, Key=object_name)
            resp_obj = S3DeleteObjectResponse(**resp)
            if resp_obj.ResponseMetadata.HTTPStatusCode != 204:
                print(resp)
        if await self.exists(bucket_name, object_name):
            return False
        return True

    async def delete(self, bucket_name: str, prefix: str) -> bool:
        if not await self.exists(bucket_name, prefix):
            print(f"bucket name: {bucket_name} prefix: {prefix} did not exist")  # TODO:
            return True

        if not prefix.endswith("/"):
            if not await self.delete_object(bucket_name, prefix):
                prefix = f"{prefix}/"

        objects = []
        async with self.session.create_s3_client() as client:
            paginator = client.get_paginator("list_objects_v2")
            async for page in paginator.paginate(
                Bucket=bucket_name, Prefix=prefix, Delimiter="/"
            ):
                _page = S3GetPaginatorResponse(**page)

                for c in _page.Contents:
                    objects.append({"Key": c.Key})

                for p in _page.CommonPrefixes:
                    await self.delete(bucket_name, p.Prefix)

                resp = await client.delete_objects(
                    Bucket=bucket_name, Delete={"Objects": objects}
                )

                resp_obj = S3DeleteObjectsResponse(**resp)

                for error in resp_obj.Errors:
                    # TODO: raise error?
                    print(error)

                objects = []

        return await self.delete_object(bucket_name, prefix)
