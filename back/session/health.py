from urllib.parse import urljoin

import httpx
from back.model.airflow import AirflowHealthResponse
from back.model.elastic import ElasticsearchHealthResponse
from back.settings import setting
from back.utils.url import get_host

airflow_host = setting.airflow_host
elasticsearch_hosts = setting.elastic_hosts


async def is_airflow_healthy() -> bool:
    healthy = "healthy"

    host = get_host(airflow_host, endswith_slash=True)
    url = urljoin(host, "health")

    print(f"airflow url: {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            return False
        resp = resp.json()
        resp = AirflowHealthResponse(**resp)

    if resp.metadatabase.status != healthy:
        return False
    if resp.scheduler.status != healthy:
        return False

    return True


async def is_elasticsearch_healthy() -> bool:
    for host in elasticsearch_hosts:
        host = get_host(host, endswith_slash=True)
        url = urljoin(host, "_cluster/health?pretty")
        print(f"elasticsearch url: {url}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                return False
            resp = resp.json()
            resp = ElasticsearchHealthResponse(**resp)
        if resp.status == "red":
            return False

    return True
