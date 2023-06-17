import socket

import httpx
from back.init.database import init_table
from back.model.service import ServiceEnum
from back.service import services
from back.session.async_elasticsearch import async_elasticsearch
from back.session.async_redis import async_redis
from back.session.storage import ping_storage as _ping_storage
from back.settings import setting
from redis import ConnectionError

AIRFLOW_HOST = setting.airflow_host


def check_host_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


async def ping_airflow() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            await client.get(AIRFLOW_HOST)
        services[ServiceEnum.AIRFLOW.value] = True
    except httpx.ConnectError:
        services[ServiceEnum.AIRFLOW.value] = False
    return services[ServiceEnum.AIRFLOW.value]


async def ping_elasticsearch() -> bool:
    services[ServiceEnum.ELASTICSEARCH.value] = await async_elasticsearch.ping()
    return services[ServiceEnum.ELASTICSEARCH.value]


async def ping_postgres() -> bool:
    try:
        await init_table()
        services[ServiceEnum.POSTGRES.value] = True
    except ConnectionRefusedError:
        services[ServiceEnum.POSTGRES.value] = False
    return services[ServiceEnum.POSTGRES.value]


async def ping_redis() -> bool:
    try:
        await async_redis.ping()
        services[ServiceEnum.REDIS.value] = True
    except ConnectionError:
        services[ServiceEnum.REDIS.value] = False
    return services[ServiceEnum.REDIS.value]


async def ping_storage() -> bool:
    services[ServiceEnum.STORAGE.value] = await _ping_storage()
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
