import io
import json
from collections import deque
from pathlib import Path
from typing import Deque, List, Tuple

from aiobotocore.httpsession import EndpointConnectionError
from aiobotocore.session import AioSession, ClientCreatorContext

from back.model.base import SourceBaseModel, SourceProtocolEnum
from back.model.s3 import (
    S3DeleteObjectResponse,
    S3DeleteObjectsResponse,
    S3GetObjectResponse,
    S3GetPaginatorResponse,
    S3ListBucketsResponse,
    S3Object,
    S3PutObjectResponse,
    S3Response,
)
from back.model.storage import (
    StorageGalleries,
    StorageGallery,
    StorageGalleryCodeEnum,
    StorageStat,
)
from back.settings import setting
from back.utils.fs import alphanum_sorting
from back.utils.image import is_browser_image, is_image
from back.utils.video import is_video

BUCKET_NAMES = [setting.storage_cache]

STORAGE_S3_AWS_ACCESS_KEY_ID = setting.storage_s3_aws_access_key_id
STORAGE_S3_AWS_SECRET_ACCESS_KEY = setting.storage_s3_aws_secret_access_key
STORAGE_S3_ENDPOINT_URL = setting.storage_s3_endpoint_url


def get_source(
    bucket_name: str,
    prefix: str,
    protocol: SourceProtocolEnum = SourceProtocolEnum.MINIO.value,
) -> SourceBaseModel:
    if bucket_name[-1] == "/":
        bucket_name = bucket_name[:-1]

    # Prefix should not start with "/".
    if len(prefix) > 0 and prefix[0] == "/":
        prefix = prefix[1:]

    path = f"{protocol}://{bucket_name}/{prefix}"
    return SourceBaseModel(path=path)


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

    if not bucket_name or bucket_name == "/":
        _resp = await client.list_buckets()
        resp = S3ListBucketsResponse(**_resp)
        for b in resp.Buckets:
            prefixes.append(S3Object(bucket_name=b.Name))
        return prefixes

    paginator = client.get_paginator("list_objects_v2")
    async for page in paginator.paginate(
        Bucket=bucket_name, Prefix=prefix, Delimiter="/", MaxKeys=1000
    ):
        _page = S3GetPaginatorResponse(**page)
        for c in _page.Contents:
            prefixes.append(S3Object(bucket_name=_page.Name, prefix=c.Key))
        for p in _page.CommonPrefixes:
            prefixes.append(S3Object(bucket_name=_page.Name, prefix=p.Prefix))
    return prefixes


async def list_filenames(
    client, bucket_name: str, prefix: str, delimiter: str = "/"
) -> List[str]:
    _predix = prefix
    if not prefix.endswith("/"):
        _predix += "/"

    filenames = []

    paginator = client.get_paginator("list_objects_v2")
    async for page in paginator.paginate(
        Bucket=bucket_name, Prefix=_predix, Delimiter=delimiter, MaxKeys=1000
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
        Bucket=bucket_name, Prefix=prefix, Delimiter="/", MaxKeys=1000
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


async def iter_prefixes(client, bucket_name: str, prefix: str, depth: int):
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
            async for obj in iter_prefixes(client, bucket_name, obj.prefix, depth):
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

        try:
            resp = await client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=object_name_with_delimiter,
                Delimiter="/",
                MaxKeys=1,
            )
        except client.exceptions.NoSuchBucket:
            return False

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
        Bucket=bucket_name, Prefix=_prefix, Delimiter="/", MaxKeys=1000
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
                self.aws_access_key_id = STORAGE_S3_AWS_ACCESS_KEY_ID
            if self.aws_secret_access_key is None:
                self.aws_secret_access_key = STORAGE_S3_AWS_SECRET_ACCESS_KEY
            if self.endpoint_url is None:
                self.endpoint_url = STORAGE_S3_ENDPOINT_URL

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

    async def are_galleries(
        self, source: SourceBaseModel, depth: int
    ) -> StorageGalleries:
        s = StorageGalleries()
        if depth > 0:
            count_galleries = 0
            total = 0
            stack: Deque[Tuple[int, S3Object]] = deque([])
            stack.append(
                (
                    depth,
                    S3Object(bucket_name=source.bucket_name, prefix=source.object_name),
                )
            )

            while stack:
                d, s3_object = stack.popleft()
                bucket_name = s3_object.bucket_name
                prefix = s3_object.prefix

                g_source = get_source(
                    source.bucket_name,
                    prefix=prefix,
                    protocol=source.protocol,
                )

                if d == 0:
                    total += 1

                    if not prefix.endswith("/"):
                        prefix += "/"

                    paginator = self.client.get_paginator("list_objects_v2")
                    async for page in paginator.paginate(
                        Bucket=bucket_name, Prefix=prefix, Delimiter="/", MaxKeys=1000
                    ):
                        p_0 = S3GetPaginatorResponse(**page)
                        for c in p_0.Contents:
                            p = c.Key
                            if is_browser_image(Path(p)):
                                count_galleries += 1
                                break
                        else:
                            g = StorageGallery(
                                path=g_source.path,
                                code=StorageGalleryCodeEnum.DOES_NOT_HAVE_IMAGES.value,
                            )
                            s.galleries.append(g)
                    continue

                if not bucket_name or bucket_name == "/":
                    _resp = await self.client.list_buckets()
                    resp = S3ListBucketsResponse(**_resp)
                    for b in resp.Buckets:
                        stack.append((d - 1, S3Object(bucket_name=b.Name)))
                    continue

                paginator = self.client.get_paginator("list_objects_v2")
                async for page in paginator.paginate(
                    Bucket=bucket_name, Prefix=prefix, Delimiter="/", MaxKeys=1000
                ):
                    p_1 = S3GetPaginatorResponse(**page)
                    if len(p_1.Contents) > 0:
                        g = StorageGallery(
                            path=g_source.path,
                            code=StorageGalleryCodeEnum.FILES_IN_THE_INTERNAL_NODES_OF_THE_STORAGE_PATH.value,
                        )
                        s.galleries.append(g)
                    for p in p_1.CommonPrefixes:
                        stack.append(
                            (
                                d - 1,
                                S3Object(bucket_name=p_1.Name, prefix=p.Prefix),
                            )
                        )

            if total != 0:
                s.percentage = count_galleries / total
            return s

        raise ValueError("depth should be greater than 0.")

    async def init(self):
        for bucket_name in BUCKET_NAMES:
            try:
                await self.client.head_bucket(Bucket=bucket_name)
            except self.client.exceptions.ClientError:
                await self.client.create_bucket(Bucket=bucket_name)

    async def ping(self) -> bool:
        try:
            _resp = await self.client.list_buckets()
        except (self.client.exceptions.ClientError, EndpointConnectionError):
            return False
        resp = S3Response(**_resp)
        if resp.ResponseMetadata.HTTPStatusCode == 200:
            return True
        return False

    async def get_url(self, source: SourceBaseModel) -> str:
        return await generate_presigned_url(
            self.client, source.bucket_name, source.object_name
        )

    async def get_object(self, source: SourceBaseModel) -> bytes:
        return await get_object(self.client, source.bucket_name, source.object_name)

    async def get_json(self, source: SourceBaseModel) -> dict:
        obj = await self.get_object(source)
        if obj is None:
            return None
        return json.loads(obj)

    async def get_storage_stat(
        self, source: SourceBaseModel, depth: int
    ) -> StorageStat:
        _bucket_name = source.bucket_name
        _predix = source.object_name

        if _bucket_name.endswith("/"):
            _bucket_name = _bucket_name[:-1]

        if _predix is None:
            _predix = "/"
        elif not _predix.endswith("/"):
            _predix += "/"

        _base_path = f"{_bucket_name}{_predix}"
        _base_depth = len(_base_path.split("/"))
        _image_depth = _base_depth + depth
        _gallery_depth = _image_depth - 1

        stat = StorageStat()
        _galleries_cache = set()

        paginator = self.client.get_paginator("list_objects_v2")
        async for page in paginator.paginate(
            Bucket=_bucket_name, Prefix=_predix, Delimiter="", MaxKeys=1000
        ):
            _page = S3GetPaginatorResponse(**page)
            for c in _page.Contents:
                stat.size += c.Size
                stat.num_files += 1

                p = c.Key
                obj_path_str = f"{source.bucket_name}/{p}"
                obj_path_str_split = obj_path_str.split("/")
                obj_path = Path(obj_path_str)
                obj_depth = len(obj_path_str_split)

                gallery_path_str = "/".join(obj_path_str_split[:_gallery_depth])
                if gallery_path_str != obj_path_str:
                    _galleries_cache.add(gallery_path_str)

                if is_image(obj_path) and obj_depth == _image_depth:
                    stat.num_images += 1
                if depth == -1 and is_video(obj_path).suffix.lower() == ".mp4":
                    stat.num_mp4s += 1
        stat.num_galleries = len(_galleries_cache)
        return stat

    async def list_nested_sources(
        self, source: SourceBaseModel
    ) -> List[SourceBaseModel]:
        _bucket_name = source.bucket_name
        _predix = source.object_name
        if _predix is None:
            _predix = "/"
        elif not _predix.endswith("/"):
            _predix += "/"

        sources = []

        paginator = self.client.get_paginator("list_objects_v2")
        async for page in paginator.paginate(
            Bucket=_bucket_name, Prefix=_predix, Delimiter="", MaxKeys=1000
        ):
            _page = S3GetPaginatorResponse(**page)
            for c in _page.Contents:
                p = c.Key
                if source.storage_id is None:
                    _protocol = source.protocol
                else:
                    _protocol = f"{source.protocol}-{source.storage_id}"
                obj_path = f"{_protocol}://{source.bucket_name}/{p}"  # noqa
                obj_source = SourceBaseModel(path=obj_path)
                sources.append(obj_source)

        return sources

    async def list_filenames(self, source: SourceBaseModel) -> List[str]:
        return await list_filenames(self.client, source.bucket_name, source.object_name)

    async def list_images(self, source: SourceBaseModel) -> List[str]:
        filenames = await list_filenames(
            self.client, source.bucket_name, source.object_name
        )
        images = [
            filename for filename in filenames if is_browser_image(Path(filename))
        ]
        images.sort(key=alphanum_sorting)

        return images

    async def iter_directories(self, source: SourceBaseModel, depth: int):
        async for obj in iter_prefixes(
            self.client, source.bucket_name, source.object_name, depth
        ):
            if obj is not None:
                obj_path = f"{source.protocol}-{source.storage_id}://{source.bucket_name}/{obj.prefix}"  # noqa
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
