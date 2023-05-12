from typing import Any, Generic, List

from back.model.elastic import AnalyzerEnum, SearchResult, SourceT
from back.session.async_elasticsearch import async_elastic
from back.settings import setting
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException

ELASTICSEARCH_SIZE = setting.elastic_size


class CrudAsyncElasticsearchBase(Generic[SourceT]):
    def __init__(
        self,
        hosts: List[str] = None,
        size: int = 10,
        index: str = None,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        sorting: List[Any] = ["_score"],
        is_from_setting_if_none: bool = False,
    ):
        if analyzer not in [a.value for a in AnalyzerEnum]:
            raise HTTPException(status=404, detail=f"Analyzer: {analyzer} not found")
        self.hosts = hosts
        self.size = size
        self.index = index
        self.async_elasticsearch = AsyncElasticsearch(hosts=hosts)

        if is_from_setting_if_none:
            self.init_from_setting()

    def init_from_setting(self):
        if self.hosts is None:
            self.async_elasticsearch = async_elastic
        self.size = ELASTICSEARCH_SIZE

    async def iter(self) -> SearchResult[SourceT]:
        dsl = {
            "size": self.size,
            "query": {"match_all": {}},
            "track_total_hits": True,
            "sort": ["_doc"],
        }
        _resp = await self.async_elasticsearch.search(
            index=self.index, body=dsl, scroll="1m"
        )
        resp = SearchResult[SourceT](**_resp)
        yield resp

        while resp.hits.hits:
            _resp = await self.async_elasticsearch.scroll(
                scroll_id=resp.scroll_id, scroll="1m"
            )
            resp = SearchResult[SourceT](**_resp)
            if resp.hits.hits:
                yield resp
