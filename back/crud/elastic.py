from typing import Any, Generic, List

from back.model.elastic import AnalyzerEnum, Count, QueryBoolean, SearchResult, SourceT
from back.session.elastic import elastic_client
from back.settings import setting
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import HTTPException
from pydantic import BaseModel

index = setting.elastic_index_gallery
batch_size = 300
es_size = setting.elastic_size

ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW = 10000


class CrudElasticBase(Generic[SourceT]):
    def __init__(
        self,
        elastic_client: Elasticsearch = elastic_client,
        size: int = es_size,
        index: str = index,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        sorting: List[Any] = ["_score"],
    ):
        if analyzer not in [a.value for a in AnalyzerEnum]:
            raise HTTPException(status=404, detail=f"Analyzer: {analyzer} not found")

        self.analyzer = analyzer.value
        self.elastic_client = elastic_client
        self.index = index
        self.size = size

        self.sorting = sorting

    @property
    def fields(self) -> List[str]:
        raise NotImplementedError()

    def advanced_search(self, *args, **kwargs):
        raise NotImplementedError()

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

    def get_total(self) -> int:
        return self.match_all(1).hits.total.value

    def get_from(self, page: int) -> int:
        if page > 0:
            return (page - 1) * self.size
        return 0

    def query(self, page: int, dsl: dict) -> SearchResult[SourceT]:
        target_idx = page * self.size
        max_page = ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW // self.size

        if target_idx > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW:
            current_page = max_page

            dsl["from"] = self.get_from(current_page)

            hits = self.elastic_client.search(index=self.index, body=dsl)
            total = hits["hits"]["total"]["value"]

            if page > (total // self.size + 1):
                galleries = SearchResult[SourceT](**{"hits": {}})
            else:
                page -= max_page

                dsl["from"] = 0

                while page > 1:
                    if page > max_page:
                        p = max_page
                    else:
                        p = page - 1

                    dsl["size"] = self.size * p
                    dsl["search_after"] = hits["hits"]["hits"][-1]["sort"]

                    hits = self.elastic_client.search(index=self.index, body=dsl)

                    page -= p

                dsl["size"] = self.size
                dsl["search_after"] = hits["hits"]["hits"][-1]["sort"]

                hits = self.elastic_client.search(index=self.index, body=dsl)
                galleries = SearchResult[SourceT](**hits)

        else:
            dsl["from"] = self.get_from(page)
            hits = self.elastic_client.search(index=self.index, body=dsl)
            galleries = SearchResult[SourceT](**hits)

        return galleries

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
                                    "analyzer": self.analyzer,
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
                                    "analyzer": self.analyzer,
                                }
                            }
                        }
                    }
                    for keyword in keywords
                ]
            }
        }

    def custom(self, body: dict) -> dict:
        return self.elastic_client.search(index=self.index, body=body)

    def count(self, body: dict) -> Count:
        return Count(**self.elastic_client.count(index=self.index, body=body))

    def match_by_query(self, dsl: dict, page: int) -> SearchResult[SourceT]:
        dsl = self.get_basic_dsl(dsl=dsl)
        return self.query(page, dsl)

    def match(
        self,
        page: int,
        keywords: str,
        fuzziness: int = 0,
        boolean: QueryBoolean = QueryBoolean.SHOULD,
    ) -> SearchResult[SourceT]:
        dsl = self.get_basic_dsl()

        if boolean == QueryBoolean.SHOULD:
            dsl["query"] = self.get_should_match_query(keywords, fuzziness=fuzziness)
        elif boolean == QueryBoolean.MUST:
            dsl["query"] = self.get_must_match_query(keywords, fuzziness=fuzziness)

        return self.query(page, dsl)

    def match_all(self, page: int) -> SearchResult[SourceT]:
        dsl = self.get_basic_dsl()
        dsl["query"] = {"match_all": {}}
        return self.query(page, dsl)

    def random(
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

        return self.query(page, dsl)


def get_source_by_id(
    id: str,
    model: BaseModel,
    elastic_client: Elasticsearch = elastic_client,
    index: str = index,
) -> BaseModel:
    try:
        hit = elastic_client.get(index=index, id=id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Gallery not found")

    source = hit.get("_source", None)
    if source is None:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return model(**source)
