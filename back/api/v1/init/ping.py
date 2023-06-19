from back.dependency.security import api_security
from back.init.check import (
    ping,
    ping_airflow,
    ping_elasticsearch,
    ping_postgres,
    ping_redis,
    ping_storage,
)
from back.model.base import SourceProtocolEnum
from back.model.scope import ScopeEnum
from fastapi import APIRouter, Query

router = APIRouter(prefix="/ping")


@router.get(
    "/services",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.init_ping_services_get.name])],
)
async def get_ping_services() -> bool:
    return await ping()


@router.post(
    "/airflow",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.init_ping_airflow_post.name])],
)
async def post_ping_airflow(
    airflow_host: str = Query(
        default=None,
        example="http://localhost:8080",
    ),
    airflow_username: str = Query(default=None),
    airflow_password: str = Query(default=None),
) -> bool:
    if airflow_host is None:
        return await ping_airflow()
    return await ping_airflow(
        airflow_host=airflow_host,
        airflow_username=airflow_username,
        airflow_password=airflow_password,
    )


@router.post(
    "/elasticsearch",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.init_ping_elasticsearch_post.name])],
)
async def post_ping_elasticsearch(
    hosts: str = Query(
        default=None,
        examples={
            "Single node": {"summary": "Single node", "value": "http://localhost:9200"},
            "Cluster": {
                "summary": "Cluster",
                "description": "We use `,` to separate the hosts.",
                "value": "http://node-1:9200,http://node-2:9200",
            },
        },
    )
) -> bool:
    if hosts is None:
        return await ping_elasticsearch()
    _hosts = hosts.split(",")
    return await ping_elasticsearch(hosts=_hosts)


@router.post(
    "/postgres",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.init_ping_postgres_post.name])],
)
async def post_ping_postgres(
    database_url: str = Query(
        default=None,
        example="postgresql+asyncpg://zetsubou:zetsubou@localhost:5430/zetsubou",
    )
) -> bool:
    if database_url is None:
        return await ping_postgres()
    return await ping_postgres(database_url=database_url)


@router.post(
    "/redis",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.init_ping_redis_post.name])],
)
async def post_ping_redis(
    redis_url: str = Query(
        default=None,
        example="redis://localhost:6380/0",
    )
) -> bool:
    if redis_url is None:
        return await ping_redis()
    return await ping_redis(redis_url=redis_url)


@router.post(
    "/storage",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.init_ping_storage_post.name])],
)
async def post_ping_storage(
    storage_protocol: SourceProtocolEnum = None,
    storage_s3_aws_access_key_id: str = Query(
        default=None, title="S3 AWS Access Key ID / MinIO Root User"
    ),
    storage_s3_aws_secret_access_key: str = Query(
        default=None, title="S3 AWS Secret Access Key / MinIO Root Password"
    ),
    storage_s3_endpoint_url: str = Query(
        default=None,
        example="http://localhost:9000",
    ),
) -> bool:
    if (
        storage_protocol is None
        and storage_s3_aws_access_key_id is None
        and storage_s3_aws_secret_access_key is None
        and storage_s3_endpoint_url is None
    ):
        return await ping_storage()
    return await ping_storage(
        storage_protocol=storage_protocol,
        storage_s3_aws_access_key_id=storage_s3_aws_access_key_id,
        storage_s3_aws_secret_access_key=storage_s3_aws_secret_access_key,
        storage_s3_endpoint_url=storage_s3_endpoint_url,
    )
