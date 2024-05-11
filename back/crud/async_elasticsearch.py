from collections import deque
from typing import Any, AsyncGenerator, Dict, Generic, List, Optional, Set, Tuple

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import async_scan
from fastapi import HTTPException

from back.model.elasticsearch import (
    ElasticsearchAnalyzerEnum,
    ElasticsearchCountResult,
    ElasticsearchQueryBooleanEnum,
    SourceT,
)
from back.session.async_elasticsearch import get_async_elasticsearch
from back.settings import setting
from back.utils.keyword import KeywordParser

ELASTICSEARCH_SIZE = setting.elastic_size
ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW = 10000


class CrudAsyncElasticsearchBase(Generic[SourceT]):
    def __init__(
        self,
        hosts: Optional[List[str]] = None,
        index: Optional[str] = None,
        keyword_analyzers: Dict[ElasticsearchAnalyzerEnum, List[str]] = {},
        sorting: List[Any] = [
            "_score",
            {"last_updated": {"order": "desc", "unmapped_type": "long"}},
        ],
        is_from_setting_if_none: bool = False,
    ):
        for analyzer in keyword_analyzers.keys():
            if analyzer not in [a.value for a in ElasticsearchAnalyzerEnum]:
                raise HTTPException(
                    status_code=404, detail=f"Analyzer: {analyzer} not found"
                )
        self.keyword_analyzers = keyword_analyzers

        self.hosts = hosts
        self.index = index
        self.async_elasticsearch = AsyncElasticsearch(hosts=hosts)

        self.sorting = sorting

        if is_from_setting_if_none:
            self.init_from_setting()

    def init_from_setting(self):
        if self.hosts is None:
            self.async_elasticsearch = get_async_elasticsearch()

    async def close(self):
        await self.async_elasticsearch.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def get_by_id(self, id: str) -> SourceT:
        raise NotImplementedError()

    async def advanced_search(self, *args, **kwargs):
        raise NotImplementedError()

    async def match_phrase_prefix(self, keywords: str, size: int = ELASTICSEARCH_SIZE):
        raise NotImplementedError()

    async def iter(self, size) -> AsyncGenerator[dict, None]:
        dsl = {
            "size": size,
            "query": {"match_all": {}},
            "track_total_hits": True,
            "sort": [
                "_doc",
            ],
        }
        async for doc in async_scan(
            client=self.async_elasticsearch, query=dsl, index=self.index
        ):
            # resp = ElasticsearchSearchResult[SourceT](**doc)
            yield doc

    def get_keyword_fields(self, analyzer: ElasticsearchAnalyzerEnum) -> List[str]:
        if type(analyzer) is not str:
            analyzer = analyzer.value
        return self.keyword_analyzers.get(analyzer, [])

    async def get_field_names(self) -> Set[str]:
        resp = await self.async_elasticsearch.indices.get_mapping(index=self.index)
        mappings = resp.get(self.index, {}).get("mappings", None)
        if mappings is None:
            return set()
        field_names = set()
        stack = deque([(mappings, "")])
        while stack:
            current_mappings, parent_field_name = stack.popleft()
            properties = current_mappings.get("properties", None)

            if properties is None:
                field_names.add(parent_field_name)
                continue

            for field_name, next_mappings in properties.items():
                if parent_field_name:
                    stack.append((next_mappings, f"{parent_field_name}.{field_name}"))
                else:
                    stack.append((next_mappings, field_name))

        return field_names

    def get_basic_dsl(self, size: int = ELASTICSEARCH_SIZE) -> dict:
        return {
            "size": size,
            "sort": self.sorting,
            "track_total_hits": True,
        }

    def update_dsl(
        self, dsl: dict, size: int = ELASTICSEARCH_SIZE, track_total_hits: bool = True
    ) -> dict:
        if dsl.get("size", None) is None:
            dsl["size"] = size
        if dsl.get("sort", None) is None:
            dsl["sort"] = self.sorting
        if dsl.get("track_total_hits", None) is None:
            dsl["track_total_hits"] = track_total_hits
        return dsl

    def get_from(self, page: int, size: int) -> int:
        if page > 0:
            return (page - 1) * size
        return 0

    def _filter_field_names(
        self, pairs: Tuple[str, str], field_names: Set[str]
    ) -> Tuple[List[Tuple[str, str]], List[str]]:
        new_pairs = []
        remaining_keywords = []
        for name, value in pairs:
            if name in field_names:
                new_pairs.append((name, value))
            else:
                remaining_keywords.append(name)
                remaining_keywords.append(value)

        return new_pairs, remaining_keywords

    def _get_ngram_constant_score_query(
        self, keywords: List[str], fuzziness: int = 0
    ) -> List[Any]:
        _keywords_ngram = "".join(keywords)

        ngram_fields = []
        non_ngram_fields = []
        fields = self.get_keyword_fields(ElasticsearchAnalyzerEnum.NGRAM.value)
        for field in fields:
            if field.endswith(ElasticsearchAnalyzerEnum.NGRAM.value):
                ngram_fields.append(field)
            else:
                non_ngram_fields.append(field)

        ngram_constant_score_query = [
            {
                "constant_score": {
                    "filter": {
                        "multi_match": {
                            "query": keyword,
                            "fuzziness": fuzziness,
                            "fields": ngram_fields,
                        }
                    }
                }
            }
            for keyword in _keywords_ngram
        ]

        non_ngram_constant_score_query = [
            {
                "constant_score": {
                    "filter": {
                        "multi_match": {
                            "query": keyword,
                            "fuzziness": fuzziness,
                            "fields": non_ngram_fields,
                        }
                    }
                }
            }
            for keyword in keywords
        ]

        return ngram_constant_score_query + non_ngram_constant_score_query

    def _get_constant_score_query(
        self,
        keywords: str,
        keyword_analyzer: ElasticsearchAnalyzerEnum,
        fuzziness: int = 0,
    ) -> List[Any]:
        fields = self.get_keyword_fields(keyword_analyzer)
        return [
            {
                "constant_score": {
                    "filter": {
                        "multi_match": {
                            "query": keyword,
                            "fuzziness": fuzziness,
                            "fields": fields,
                        }
                    }
                }
            }
            for keyword in keywords
        ]

    async def get_match_query(
        self,
        keywords: str,
        keyword_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        fuzziness: int = 0,
        boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    ) -> dict:
        field_names = await self.get_field_names()
        parser = KeywordParser()
        parsed_keywords = parser.parse(keywords)
        remaining_keywords = parsed_keywords.remaining_keywords.split()
        includes, remaining_keywords_from_includes = self._filter_field_names(
            parsed_keywords.includes, field_names
        )
        excludes, remaining_keywords_from_excludes = self._filter_field_names(
            parsed_keywords.excludes, field_names
        )
        new_remaining_keywords = (
            remaining_keywords
            + remaining_keywords_from_includes
            + remaining_keywords_from_excludes
        )

        if keyword_analyzer == ElasticsearchAnalyzerEnum.NGRAM.value:
            constant_score_query = self._get_ngram_constant_score_query(
                new_remaining_keywords, fuzziness
            )
        else:
            constant_score_query = self._get_constant_score_query(
                new_remaining_keywords, keyword_analyzer, fuzziness
            )

        if type(boolean) is not str:
            _boolean = boolean.value
        else:
            _boolean = boolean

        for field_name, field_value in includes:
            constant_score_query.append(
                {
                    "constant_score": {
                        "filter": {
                            "multi_match": {
                                "query": field_value,
                                "fuzziness": fuzziness,
                                "fields": f"{field_name}.*",
                            }
                        }
                    }
                }
            )

        must_not = []
        for field_name, field_value in excludes:
            if field_value:
                must_not.append(
                    {"term": {f"{field_name}.keyword": {"value": field_value}}}
                )
            else:
                must_not.append({"exists": {"field": field_name}})

        return {"bool": {_boolean: constant_score_query, "must_not": must_not}}

    def add_advanced_query(
        self,
        dsl: dict,
        keywords: str,
        field_name: str,
        analyzer: ElasticsearchAnalyzerEnum,
        fuzziness: int,
        boolean: ElasticsearchQueryBooleanEnum,
    ):
        if type(analyzer) is not str:
            _analyzer = analyzer.value
        else:
            _analyzer = analyzer

        if type(boolean) is not str:
            _boolean = boolean.value
        else:
            _boolean = boolean

        _field_name = f"{field_name}.{_analyzer}"

        if analyzer == ElasticsearchAnalyzerEnum.NGRAM:
            _keywords = keywords.replace(" ", "")
        else:
            _keywords = keywords.split()

        for k in _keywords:
            dsl["query"]["bool"][_boolean].append(
                {
                    "constant_score": {
                        "filter": {
                            "multi_match": {
                                "query": k,
                                "fuzziness": fuzziness,
                                "fields": [_field_name],
                            }
                        }
                    }
                }
            )

    async def query(self, page: int, dsl: dict) -> dict:
        size = dsl.get("size", None)
        if size is None:
            raise ValueError("key `size` not found")

        target_idx = page * size
        max_page = ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW // size

        if target_idx > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW:
            current_page = max_page

            dsl["from_"] = self.get_from(current_page, size)

            _resp = await self.async_elasticsearch.search(index=self.index, **dsl)
            total = _resp["hits"]["total"]["value"]

            if page > (total // size + 1):
                _resp = {"hits": {}}
                # sources = ElasticsearchSearchResult[SourceT](**{"hits": {}})
            else:
                page -= max_page

                dsl["from_"] = 0

                while page > 1:
                    if page > max_page:
                        p = max_page
                    else:
                        p = page - 1

                    dsl["size"] = size * p
                    dsl["search_after"] = _resp["hits"]["hits"][-1]["sort"]

                    _resp = await self.async_elasticsearch.search(
                        index=self.index, **dsl
                    )

                    page -= p

                dsl["size"] = size
                dsl["search_after"] = _resp["hits"]["hits"][-1]["sort"]

                _resp = await self.async_elasticsearch.search(index=self.index, **dsl)
                # sources = ElasticsearchSearchResult[SourceT](**_resp)

        else:
            dsl["from_"] = self.get_from(page, size)
            _resp = await self.async_elasticsearch.search(index=self.index, **dsl)
            # sources = ElasticsearchSearchResult[SourceT](**_resp)

        return _resp

    async def custom(self, body: dict) -> dict:
        return await self.async_elasticsearch.search(index=self.index, **body)

    async def count(self, body: dict) -> ElasticsearchCountResult:
        _resp = await self.async_elasticsearch.count(index=self.index, body=body)
        return ElasticsearchCountResult(**_resp)

    async def random(
        self,
        page: int,
        size: int = ELASTICSEARCH_SIZE,
        keywords: str = "",
        keyword_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        fuzziness: int = 0,
        boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        seed: int = 1048596,
    ) -> dict:
        dsl = self.get_basic_dsl(size=size)
        dsl["query"] = {
            "function_score": {
                "query": {"match_all": {}},
                "random_score": {"seed": seed, "field": "id.keyword"},
            }
        }

        if keywords:
            dsl["query"]["function_score"]["query"] = dsl["query"] = (
                await self.get_match_query(
                    keywords,
                    keyword_analyzer=keyword_analyzer,
                    fuzziness=fuzziness,
                    boolean=boolean,
                )
            )

        return await self.query(page, dsl)

    async def match(
        self,
        page: int,
        size: int = ELASTICSEARCH_SIZE,
        keywords: str = "",
        keyword_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        fuzziness: int = 0,
        boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    ) -> dict:
        if keywords is None or keywords == "":
            return await self.match_all(page, size=size)

        dsl = self.get_basic_dsl(size=size)

        dsl["query"] = await self.get_match_query(
            keywords,
            keyword_analyzer=keyword_analyzer,
            fuzziness=fuzziness,
            boolean=boolean,
        )

        source = await self.query(page, dsl)
        return source

    async def match_by_query(
        self, dsl: dict, page: int, size: int = ELASTICSEARCH_SIZE
    ) -> dict:
        dsl = self.update_dsl(dsl=dsl, size=size)
        return await self.query(page, dsl)

    async def match_all(self, page: int, size: int = ELASTICSEARCH_SIZE) -> dict:
        dsl = self.get_basic_dsl(size=size)
        dsl["query"] = {"match_all": {}}
        return await self.query(page, dsl)

    async def get_total(self) -> Optional[int]:
        docs = await self.match_all(1, size=1)
        total = docs.get("hits", {}).get("total", {}).get("value", None)
        return total

    async def get_source_by_id(self, id: str) -> dict:
        try:
            _resp = await self.async_elasticsearch.get(index=self.index, id=id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"{id} not found")

        source = _resp.get("_source", None)
        if source is None:
            raise HTTPException(status_code=404, detail=f"{id} not found")
        return source

    async def get_sources_by_ids(self, ids: List[str]) -> dict:
        size = len(ids)
        dsl = {"size": size, "query": {"ids": {"values": ids}}}
        try:
            _resp = await self.async_elasticsearch.search(index=self.index, **dsl)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"{id} not found")
        # sources = ElasticsearchSearchResult[SourceT](**_resp)
        return _resp
