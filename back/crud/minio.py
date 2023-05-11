import io
import json
from datetime import timedelta
from typing import List

from back.db.crud import CrudMinioStorage
from back.model.base import SourceBaseModel
from back.model.minio import MinioObject
from back.session.minio import get_minio_client, minio_client
from back.settings import setting
from fastapi import HTTPException

from minio import Minio
from minio.deleteobjects import DeleteObject
from minio.error import S3Error

expires = timedelta(minutes=setting.minio_expires_in_minutes)


def exists(minio_client: Minio, bucket_name: str, object_name: str) -> bool:
    if object_name[-1] == "/":
        g = minio_client.list_objects(bucket_name, prefix=object_name)
        return next(g, None) is not None
    try:
        minio_client.stat_object(bucket_name, object_name)
        return True
    except S3Error:
        return False


class CrudMinio:
    def __init__(
        self, minio_client: Minio = minio_client, expires: timedelta = expires
    ):
        self.minio_client = minio_client
        self.expires = expires

    def list(
        self, bucket_name: str, prefix: str, start_after=None, limit: int = 20
    ) -> List[MinioObject]:
        if prefix is not None and len(prefix) > 0 and prefix[-1] != "/":
            return []
        if not bucket_name:
            if not prefix:
                objs = self.minio_client.list_buckets()
                return [MinioObject(bucket_name=obj.name) for obj in objs]
            else:
                # TODO: raise error
                pass
        else:
            objs = self.minio_client.list_objects(bucket_name, prefix=prefix)
            if limit is not None:
                return [
                    MinioObject(
                        bucket_name=obj.bucket_name, object_name=obj.object_name
                    )
                    for i, obj in enumerate(objs)
                    if i < limit
                ]
            return [
                MinioObject(bucket_name=obj.bucket_name, object_name=obj.object_name)
                for i, obj in enumerate(objs)
            ]

    def stat(self, bucket_name: str, object_name: str):
        return self.minio_client.stat_object(bucket_name, object_name)

    def exists(self, bucket_name: str, object_name: str) -> bool:
        return exists(self.minio_client, bucket_name, object_name)

    def put_json(
        self,
        bucket_name: str,
        object_name: str,
        data: dict,
        indent=4,
        ensure_ascii=False,
        encoding: str = "utf-8",
    ):
        data = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii).encode(
            encoding=encoding
        )
        data = io.BytesIO(data)
        self.minio_client.put_object(
            bucket_name,
            object_name,
            data,
            len(data.getvalue()),
            content_type="application/json",
        )

    def get_url(self, bucket_name: str, object_name: str):
        return self.minio_client.presigned_get_object(
            bucket_name, object_name, expires=self.expires
        )

    def delete_prefix(self, bucket_name: str, object_name: str):
        delete_object_list = map(
            lambda x: DeleteObject(x.object_name),
            self.minio_client.list_objects(bucket_name, object_name, recursive=True),
        )
        errors = self.minio_client.remove_objects(bucket_name, delete_object_list)
        for error in errors:
            print("error occured when deleting object", error)


async def get_minio_client_by_source(
    source: SourceBaseModel, crud_minio_storage: CrudMinioStorage
) -> Minio:
    minio_storage_id = source.minio_storage_id
    minio_storage = await crud_minio_storage.get_row_by_id(minio_storage_id)
    if minio_storage is None:
        raise HTTPException(
            status_code=404, detail=f"Minio storage id: {minio_storage_id} not found"
        )

    return get_minio_client(
        minio_storage.endpoint,
        access_key=minio_storage.access_key,
        secret_key=minio_storage.secret_key,
    )
