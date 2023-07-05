from typing import List
from urllib.parse import unquote

from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    EndpointResolutionError,
)
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from back.dependency.security import api_security
from back.model.s3 import S3Object
from back.model.scope import ScopeEnum
from back.session.storage.async_s3 import AsyncS3Session, list_all

router = APIRouter(tags=["Minio Operation"])


def get_bucket_name(bucket_name: str = ""):
    return unquote(bucket_name)


def get_prefix(prefix: str = ""):
    return unquote(prefix)


@router.get(
    "/list",
    response_model=List[S3Object],
    dependencies=[api_security([ScopeEnum.storage_minio_list_get.name])],
)
async def get_minio_list(
    bucket_name: str = Depends(get_bucket_name),
    prefix: str = Depends(get_prefix),
    endpoint: str = None,
    access_key: str = None,
    secret_key: str = None,
):
    if endpoint is not None and access_key is not None and secret_key is not None:
        session = AsyncS3Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint,
        )
        try:
            async with session:
                client = session.client
                return await list_all(client, bucket_name, prefix)
        except (EndpointConnectionError, ClientError, EndpointResolutionError):
            raise HTTPException(
                status_code=401,
                detail="Failed to login MinIO.",
            )
    return []
