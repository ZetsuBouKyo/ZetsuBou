from elasticsearch import AsyncElasticsearch

from back.settings import setting

HOSTS = setting.elastic_hosts

async_elasticsearch = AsyncElasticsearch(hosts=HOSTS)
