from collections import deque
from typing import Any, AsyncGenerator, Generic, List, Set, Tuple

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import async_scan
from fastapi import HTTPException

from back.model.elasticsearch import AnalyzerEnum, Count, QueryBooleanEnum, SourceT
from back.session.async_elasticsearch import get_async_elasticsearch
from back.settings import setting
from back.utils.keyword import KeywordParser

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
            {"last_updated": {"order": "desc", "unmapped_type": "long"}},
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
            self.async_elasticsearch = get_async_elasticsearch()
        if self.size is None:
            self.size = ELASTICSEARCH_SIZE

    async def close(self):
        await self.async_elasticsearch.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    @property
    def fields(self) -> List[str]:
        raise NotImplementedError()

    async def get_by_id(self) -> SourceT:
        raise NotImplementedError()

    async def advanced_search(self, *args, **kwargs):
        raise NotImplementedError()

    async def match_phrase_prefix(self, keywords: str, size: int = 5):
        raise NotImplementedError()

    async def iter(self) -> AsyncGenerator[dict]:
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
            # resp = SearchResult[SourceT](**doc)
            yield doc

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
        for field in self.fields:
            if field.endswith(AnalyzerEnum.NGRAM.value):
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

    def _get_constant_score_query(self, keywords: str, fuzziness: int = 0) -> List[Any]:
        return [
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

    async def get_match_query(
        self,
        keywords: str,
        fuzziness: int = 0,
        boolean: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
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

        if self.analyzer == AnalyzerEnum.NGRAM.value:
            constant_score_query = self._get_ngram_constant_score_query(
                new_remaining_keywords, fuzziness
            )
        else:
            constant_score_query = self._get_constant_score_query(
                new_remaining_keywords, fuzziness
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
        analyzer: AnalyzerEnum,
        fuzziness: int,
        boolean: QueryBooleanEnum,
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

        if analyzer == AnalyzerEnum.NGRAM:
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
        target_idx = page * self.size
        max_page = ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW // self.size

        if target_idx > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW:
            current_page = max_page

            dsl["from"] = self.get_from(current_page)

            _resp = await self.async_elasticsearch.search(index=self.index, body=dsl)
            total = _resp["hits"]["total"]["value"]

            if page > (total // self.size + 1):
                _resp = {"hits": {}}
                # sources = SearchResult[SourceT](**{"hits": {}})
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
                # sources = SearchResult[SourceT](**_resp)

        else:
            dsl["from"] = self.get_from(page)
            _resp = await self.async_elasticsearch.search(index=self.index, body=dsl)
            # sources = SearchResult[SourceT](**_resp)

        return _resp

    async def custom(self, body: dict) -> dict:
        return await self.advanced_search(index=self.index, body=body)

    async def count(self, body: dict) -> Count:
        _resp = await self.async_elasticsearch.count(index=self.index, body=body)
        return Count(**_resp)

    async def random(
        self,
        page: int,
        keywords: str = "",
        fuzziness: int = 0,
        boolean: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
        seed: int = 1048596,
    ) -> dict:
        dsl = self.get_basic_dsl()
        dsl["query"] = {
            "function_score": {
                "query": {"match_all": {}},
                "random_score": {"seed": seed, "field": "id.keyword"},
            }
        }

        if keywords:
            dsl["query"]["function_score"]["query"] = dsl[
                "query"
            ] = await self.get_match_query(
                keywords, fuzziness=fuzziness, boolean=boolean
            )

        return await self.query(page, dsl)

    async def match_by_query(self, dsl: dict, page: int) -> dict:
        dsl = self.get_basic_dsl(dsl=dsl)
        return await self.query(page, dsl)

    async def match(
        self,
        page: int,
        keywords: str,
        fuzziness: int = 0,
        boolean: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
    ) -> dict:
        if keywords is None or keywords == "":
            return await self.match_all(page)

        dsl = self.get_basic_dsl()

        dsl["query"] = await self.get_match_query(
            keywords, fuzziness=fuzziness, boolean=boolean
        )

        source = await self.query(page, dsl)
        return source

    async def match_all(self, page: int) -> dict:
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

    async def get_sources_by_ids(self, ids: List[str]) -> dict:
        dsl = {"size": self.size, "query": {"ids": {"values": ids}}}
        try:
            _resp = await self.async_elasticsearch.search(index=self.index, body=dsl)
        except NotFoundError:
            raise HTTPException(status_code=404, detail=f"{id} not found")
        # sources = SearchResult[SourceT](**_resp)
        return _resp
