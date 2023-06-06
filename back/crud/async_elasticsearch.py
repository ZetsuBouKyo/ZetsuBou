from typing import Any, Generic, List

from back.model.elasticsearch import (
    AnalyzerEnum,
    Count,
    QueryBoolean,
    SearchResult,
    SourceT,
)
from back.session.async_elasticsearch import async_elasticsearch
from back.settings import setting
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import async_scan
from fastapi import HTTPException

ELASTICSEARCH_SIZE = setting.elastic_size
ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW = 10000


class CrudAsyncElasticsearchBase(Generic[SourceT]):
    def __init__(
        self,
        hosts: List[str] = None,
        size: int = None,
        index: str = None,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        sorting: List[Any] = [
            "_score",
            {"timestamp": {"order": "desc", "unmapped_type": "long"}},
        ],
        is_from_setting_if_none: bool = False,
    ):
        if analyzer not in [a.value for a in AnalyzerEnum]:
            raise HTTPException(status=404, detail=f"Analyzer: {analyzer} not found")
        self.hosts = hosts
        self.index = index
        self.async_elasticsearch = AsyncElasticsearch(hosts=hosts)

        self.analyzer = analyzer.value
        self.sorting = sorting
        self.size = size

        if is_from_setting_if_none:
            self.init_from_setting()

    def init_from_setting(self):
        if self.hosts is None:
            self.async_elasticsearch = async_elasticsearch
        if self.size is None:
            self.size = ELASTICSEARCH_SIZE

    @property
    def fields(self) -> List[str]:
        raise NotImplementedError()

    async def get_by_id(self) -> SourceT:
        raise NotImplementedError()

    async def advanced_search(self, *args, **kwargs):
        raise NotImplementedError()

    async def match_phrase_prefix(
        self, keywords: str, size: int = 5
    ) -> SearchResult[SourceT]:
        raise NotImplementedError()

    async def iter(self) -> SearchResult[SourceT]:
        dsl = {
            "size": self.size,
            "query": {"match_all": {}},
            "track_total_hits": True,
            "sort": [
                "_doc",
            ],
        }
        async for doc in async_scan(
            client=self.async_elasticsearch, query=dsl, index=self.index
        ):
            resp = SearchResult[SourceT](**doc)
            yield resp

    def get_basic_dsl(self, dsl: dict = None) -> dict:
        if dsl is None:
            return {
                "size": self.size,
                "sort": self.sorting,
                "track_total_hits": True,
            }
        if dsl.get("size", None) is None:
            dsl["size"] = self.size
        if dsl.get("sort", None) is None:
            dsl["sort"] = self.sorting
        if dsl.get("track_total_hits", None) is None:
            dsl["track_total_hits"] = True
        return dsl

    def get_from(self, page: int) -> int:
        if page > 0:
            return (page - 1) * self.size
        return 0

    def get_must_match_query(self, keywords: str, fuzziness: int = 0) -> dict:
        keywords = keywords.split()
        return {
            "bool": {
                "must": [
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": keyword,
                                    "fuzziness": fuzziness,
                                    "fields": self.fields,
                                }
                            }
                        }
                    }
                    for keyword in keywords
                ]
            }
        }

    def get_should_match_query(self, keywords: str, fuzziness: int = 0) -> dict:
        keywords = keywords.split()
        return {
            "bool": {
                "should": [
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": keyword,
                                    "fuzziness": fuzziness,
                                    "fields": self.fields,
                                }
                            }
                        }
                    }
                    for keyword in keywords
                ]
            }
        }

    async def query(self, page: int, dsl: dict) -> SearchResult[SourceT]:
        target_idx = page * self.size
        max_page = ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW // self.size

        if target_idx > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW:
            current_page = max_page

            dsl["from"] = self.get_from(current_page)

            _resp = await self.async_elasticsearch.search(index=self.index, body=dsl)
            total = _resp["hits"]["total"]["value"]

            if page > (total // self.size + 1):
                sources = SearchResult[SourceT](**{"hits": {}})
            else:
                page -= max_page

                dsl["from"] = 0

                while page > 1:
                    if page > max_page:
                        p = max_page
                    else:
                        p = page - 1

                    dsl["size"] = self.size * p
                    dsl["search_after"] = _resp["hits"]["hits"][-1]["sort"]

                    _resp = await self.async_elasticsearch.search(
                        index=self.index, body=dsl
                    )

                    page -= p

                dsl["size"] = self.size
                dsl["search_after"] = _resp["hits"]["hits"][-1]["sort"]

                _resp = await self.async_elasticsearch.search(
                    index=self.index, body=dsl
                )
                sources = SearchResult[SourceT](**_resp)

        else:
            dsl["from"] = self.get_from(page)
            _resp = await self.async_elasticsearch.search(index=self.index, body=dsl)
            sources = SearchResult[SourceT](**_resp)

        await self.async_elasticsearch.close()

        return sources

    async def custom(self, body: dict) -> dict:
        return await self.advanced_search.search(index=self.index, body=body)

    async def count(self, body: dict) -> Count:
        _resp = await self.async_elasticsearch.count(index=self.index, body=body)
        return Count(**_resp)

    async def random(
        self,
        page: int,
        keywords: str = "",
        fuzziness: int = 0,
        boolean: QueryBoolean = QueryBoolean.SHOULD,
        seed: int = 1048596,
    ) -> SearchResult[SourceT]:
        dsl = self.get_basic_dsl()
        dsl["query"] = {
            "function_score": {
                "query": {"match_all": {}},
                "random_score": {"seed": seed, "field": "id.keyword"},
            }
        }

        if keywords:
            if boolean == QueryBoolean.SHOULD:
                dsl["query"]["function_score"]["query"] = self.get_should_match_query(
                    keywords, fuzziness=fuzziness
                )
            elif boolean == QueryBoolean.MUST:
                dsl["query"]["function_score"]["query"] = self.get_must_match_query(
                    keywords, fuzziness=fuzziness
                )

        return await self.query(page, dsl)

    async def match_by_query(self, dsl: dict, page: int) -> SearchResult[SourceT]:
        dsl = self.get_basic_dsl(dsl=dsl)
        return await self.query(page, dsl)

    async def match(
        self,
        page: int,
        keywords: str,
        fuzziness: int = 0,
        boolean: QueryBoolean = QueryBoolean.SHOULD,
    ) -> SearchResult[SourceT]:
        if keywords is None or keywords == "":
            return await self.match_all(page)

        dsl = self.get_basic_dsl()

        if boolean == QueryBoolean.SHOULD:
            dsl["query"] = self.get_should_match_query(keywords, fuzziness=fuzziness)
        elif boolean == QueryBoolean.MUST:
            dsl["query"] = self.get_must_match_query(keywords, fuzziness=fuzziness)

        return await self.query(page, dsl)

    async def match_all(self, page: int) -> SearchResult[SourceT]:
        dsl = self.get_basic_dsl()
        dsl["query"] = {"match_all": {}}
        return await self.query(page, dsl)

    async def get_total(self) -> int:
        return await self.match_all(1).hits.total.value

    async def get_source_by_id(self, id: str) -> dict:
        try:
            _resp = await self.async_elasticsearch.get(index=self.index, id=id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"{id} not found")

        source = _resp.get("_source", None)
        if source is None:
            raise HTTPException(status_code=404, detail=f"{id} not found")
        return source
