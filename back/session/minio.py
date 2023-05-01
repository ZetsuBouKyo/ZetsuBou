from urllib.parse import urlparse

from back.settings import setting
from fastapi import HTTPException

from minio import Minio

endpoint = setting.minio_endpoint
secure = setting.minio_secure
access_key = setting.minio_user
secret_key = setting.minio_password

bucket_names = [setting.minio_cache_bucket_name, setting.minio_backup_bucket_name]


def get_minio_client(endpoint: str, access_key: str, secret_key: str) -> Minio:
    endpoint = urlparse(endpoint)
    protocol = endpoint.scheme
    if protocol == "http":
        secure = False
    elif protocol == "https":
        secure = True
    else:
        raise HTTPException(status_code=422, detail="endpoint: {endpoint}")
    endpoint = f"{endpoint.netloc}{endpoint.path}"

    return Minio(
        endpoint,
        secure=secure,
        access_key=access_key,
        secret_key=secret_key,
    )


minio_client = Minio(
    endpoint,
    secure=secure,
    access_key=access_key,
    secret_key=secret_key,
)


def init_minio():
    for bucket_name in bucket_names:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
