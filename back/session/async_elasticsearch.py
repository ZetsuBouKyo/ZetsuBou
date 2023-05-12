from back.settings import setting
from elasticsearch import AsyncElasticsearch

HOSTS = setting.elastic_hosts

async_elastic = AsyncElasticsearch(hosts=HOSTS)
