from typing import List

from elasticsearch import AsyncElasticsearch

from back.settings import setting

HOSTS = setting.elastic_hosts


def get_async_elasticsearch(hosts: List[str] = HOSTS) -> AsyncElasticsearch:
    return AsyncElasticsearch(hosts=hosts)
