from typing import List
from urllib.parse import unquote

from back.crud.minio import CrudMinio
from back.db.model import ScopeEnum
from back.dependency.security import api_security
from back.model.minio import MinioObject
from back.session.minio import get_minio_client
from back.settings import setting
from fastapi import APIRouter
from fastapi.params import Depends

router = APIRouter()
default_minio_secure = setting.minio_secure


def parse_url(s: str):
    if s is None:
        return None
    return unquote(s)


def get_bucket_name(bucket_name: str = None):
    return parse_url(bucket_name)


def get_object_name(object_name: str = None):
    return parse_url(object_name)


def get_prefix(prefix: str = None):
    return parse_url(prefix)


@router.get(
    "/list",
    response_model=List[MinioObject],
    dependencies=[api_security([ScopeEnum.minio_operation_list_get.name])],
)
def get_minio_list(
    bucket_name: str = Depends(get_bucket_name),
    prefix: str = Depends(get_prefix),
    endpoint: str = None,
    access_key: str = None,
    secret_key: str = None,
):
    if endpoint is not None and access_key is not None and secret_key is not None:
        minio_client = get_minio_client(endpoint, access_key, secret_key)
        crud = CrudMinio(minio_client=minio_client)
    else:
        crud = CrudMinio()
    return crud.list(bucket_name, prefix)


@router.get(
    "/stat", dependencies=[api_security([ScopeEnum.minio_operation_stat_get.name])]
)
def get_minio_stat(
    bucket_name: str = Depends(get_bucket_name),
    object_name: str = Depends(get_object_name),
):
    crud = CrudMinio()
    return crud.stat(bucket_name, object_name)
