import logging
import socket
from typing import List

import httpx
import redis.asyncio as _async_redis
from elasticsearch import AsyncElasticsearch
from redis import ConnectionError
from sqlalchemy.ext.asyncio import create_async_engine

from back.logging import logger_zetsubou
from back.model.service import ServiceEnum
from back.service import services
from back.session.async_airflow import AsyncAirflowSession, dags
from back.session.storage import ping_storage as _ping_storage
from back.settings import setting

AIRFLOW_HOST = setting.airflow_host
AIRFLOW_USERNAME = setting.airflow_username
AIRFLOW_PASSWORD = setting.airflow_password

ELASTICSEARCH_HOSTS = setting.elastic_hosts

DATABASE_URL = setting.database_url
ECHO = setting.database_echo

REDIS_URL = setting.redis_url

STORAGE_PROTOCOL = setting.storage_protocol
STORAGE_S3_AWS_ACCESS_KEY_ID = setting.storage_s3_aws_access_key_id
STORAGE_S3_AWS_SECRET_ACCESS_KEY = setting.storage_s3_aws_secret_access_key
STORAGE_S3_ENDPOINT_URL = setting.storage_s3_endpoint_url


def check_host_port(port: int) -> bool:
    """
    Return `False` if host port is available.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


async def ping_airflow(
    airflow_host: str = AIRFLOW_HOST,
    airflow_username: str = AIRFLOW_USERNAME,
    airflow_password: str = AIRFLOW_PASSWORD,
) -> bool:
    if airflow_host is None or airflow_username is None or airflow_password is None:
        services[ServiceEnum.AIRFLOW.value] = False
    else:
        try:
            session = AsyncAirflowSession(
                host=airflow_host,
                username=airflow_username,
                password=airflow_password,
                is_from_setting_if_none=True,
            )
            dag_ids = list(dags.keys())
            resp = await session.get_dag_runs(dag_ids)

            if resp.status == 401:
                services[ServiceEnum.AIRFLOW.value] = False
            else:
                services[ServiceEnum.AIRFLOW.value] = True
        except httpx.ConnectError:
            services[ServiceEnum.AIRFLOW.value] = False
    if services[ServiceEnum.AIRFLOW.value] is False:
        logger_zetsubou.warning("Can't connect to Airflow")
    return services[ServiceEnum.AIRFLOW.value]


async def ping_elasticsearch(hosts: List[str] = ELASTICSEARCH_HOSTS) -> bool:
    if not hosts:
        services[ServiceEnum.ELASTICSEARCH.value] = False
        return services[ServiceEnum.ELASTICSEARCH.value]

    # https://github.com/elastic/elasticsearch-py/blob/eb9eb05a57227c0093d6fbdcc3391f4ad5e61bbe/elasticsearch/connection/base.py#L288
    # This line outputs unwanted error messages
    elasticsearch_logger = logging.getLogger("elasticsearch")
    elasticsearch_logger.disabled = True

    async_elasticsearch = AsyncElasticsearch(hosts=hosts)
    try:
        services[ServiceEnum.ELASTICSEARCH.value] = await async_elasticsearch.ping()
    except ConnectionRefusedError:
        services[ServiceEnum.ELASTICSEARCH.value] = False

    elasticsearch_logger.disabled = False

    await async_elasticsearch.close()

    if services[ServiceEnum.ELASTICSEARCH.value] is False:
        logger_zetsubou.warning("Can't connect to Elasticsearch")

    return services[ServiceEnum.ELASTICSEARCH.value]


async def ping_postgres(database_url: str = DATABASE_URL, echo: bool = ECHO) -> bool:
    if database_url is None:
        services[ServiceEnum.POSTGRES.value] = False
    else:
        async_engine = create_async_engine(database_url, echo=echo)
        try:
            async with async_engine.begin():
                pass
            services[ServiceEnum.POSTGRES.value] = True
        except ConnectionRefusedError:
            services[ServiceEnum.POSTGRES.value] = False

    if services[ServiceEnum.POSTGRES.value] is False:
        logger_zetsubou.warning("Can't connect to PostgreSQL")

    return services[ServiceEnum.POSTGRES.value]


async def ping_redis(redis_url: str = REDIS_URL) -> bool:
    if redis_url is None:
        services[ServiceEnum.REDIS.value] = False
    else:
        async_redis = _async_redis.from_url(redis_url)
        try:
            pong = await async_redis.ping()
            if pong:
                services[ServiceEnum.REDIS.value] = True
            else:
                services[ServiceEnum.REDIS.value] = False
        except ConnectionError:
            services[ServiceEnum.REDIS.value] = False

    if services[ServiceEnum.REDIS.value] is False:
        logger_zetsubou.warning("Can't connect to Redis")

    return services[ServiceEnum.REDIS.value]


async def ping_storage(
    storage_protocol: str = STORAGE_PROTOCOL,
    storage_s3_aws_access_key_id: str = STORAGE_S3_AWS_ACCESS_KEY_ID,
    storage_s3_aws_secret_access_key: str = STORAGE_S3_AWS_SECRET_ACCESS_KEY,
    storage_s3_endpoint_url: str = STORAGE_S3_ENDPOINT_URL,
) -> bool:
    if (
        storage_protocol is None
        or storage_s3_aws_access_key_id is None
        or storage_s3_aws_secret_access_key is None
        or storage_s3_endpoint_url is None
    ):
        services[ServiceEnum.STORAGE.value] = False
    else:
        services[ServiceEnum.STORAGE.value] = await _ping_storage(
            storage_protocol=storage_protocol,
            storage_s3_aws_access_key_id=storage_s3_aws_access_key_id,
            storage_s3_aws_secret_access_key=storage_s3_aws_secret_access_key,
            storage_s3_endpoint_url=storage_s3_endpoint_url,
        )

    if services[ServiceEnum.STORAGE.value] is False:
        logger_zetsubou.warning("Can't connect to Storage")

    return services[ServiceEnum.STORAGE.value]


async def ping_all() -> bool:
    return all(
        [
            await ping_airflow(),
            await ping_elasticsearch(),
            await ping_postgres(),
            await ping_redis(),
            await ping_storage(),
        ]
    )


async def ping(service: ServiceEnum = None) -> bool:
    if service == ServiceEnum.AIRFLOW.value:
        return await ping_airflow()
    elif service == ServiceEnum.ELASTICSEARCH.value:
        return await ping_elasticsearch()
    elif service == ServiceEnum.POSTGRES.value:
        return await ping_postgres()
    elif service == ServiceEnum.REDIS.value:
        return await ping_redis()
    elif service == ServiceEnum.STORAGE.value:
        return await ping_storage()

    return await ping_all()
