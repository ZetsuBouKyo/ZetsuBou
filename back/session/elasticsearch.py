from back.settings import setting
from elasticsearch import Elasticsearch

HOSTS = setting.elastic_hosts
elastic_client = Elasticsearch(hosts=HOSTS)
