from typing import List

from back.db.model import ScopeEnum
from back.dependency.security import api_security
from back.model.elastic import AnalyzerEnum
from fastapi import APIRouter

from ...model.elasticsearch import ElasticsearchAnalyzer, ElasticsearchQueryExample
from ...model.gallery import query_examples

router = APIRouter()


@router.get(
    "/query-examples",
    response_model=List[ElasticsearchQueryExample],
    dependencies=[api_security([ScopeEnum.elasticsearch_query_examples_get.name])],
)
def get_query_examples():
    return [ElasticsearchQueryExample(**example) for example in query_examples.values()]


@router.get(
    "/analyzers",
    response_model=List[ElasticsearchAnalyzer],
    dependencies=[api_security([ScopeEnum.elasticsearch_analyzers_get.name])],
)
def get_analyzers():
    return [ElasticsearchAnalyzer(name=a.value) for a in AnalyzerEnum]
