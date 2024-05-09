from typing import List

from fastapi import APIRouter

from back.api.model.elasticsearch import (
    ElasticsearchAnalyzer,
    ElasticsearchQueryExample,
    query_examples,
)
from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.dependency.security import api_security
from back.model.elasticsearch import ElasticsearchAnalyzerEnum
from back.model.scope import ScopeEnum
from back.settings import setting

GALLERY_INDEX = setting.elastic_index_gallery
VIDEO_INDEX = setting.elastic_index_video

router = APIRouter(prefix="/elasticsearch", tags=["Elasticsearch"])


@router.get(
    "/query-examples",
    response_model=List[ElasticsearchQueryExample],
    dependencies=[api_security([ScopeEnum.elasticsearch_query_examples_get.value])],
)
def get_query_examples():
    return [ElasticsearchQueryExample(**example) for example in query_examples.values()]


@router.get(
    "/analyzers",
    response_model=List[ElasticsearchAnalyzer],
    dependencies=[api_security([ScopeEnum.elasticsearch_analyzers_get.value])],
)
def get_analyzers():
    return [ElasticsearchAnalyzer(name=a.value) for a in ElasticsearchAnalyzerEnum]


@router.get(
    "/gallery/field-names",
    response_model=List[str],
    dependencies=[api_security([ScopeEnum.elasticsearch_analyzers_get.value])],
)
async def get_gallery_field_names() -> List[str]:
    async with CrudAsyncElasticsearchBase(
        index=GALLERY_INDEX, is_from_setting_if_none=True
    ) as crud:
        field_names = list(await crud.get_field_names())
        field_names.sort()
    return field_names


@router.get(
    "/video/field-names",
    response_model=List[str],
    dependencies=[api_security([ScopeEnum.elasticsearch_analyzers_get.value])],
)
async def get_video_field_names() -> List[str]:
    async with CrudAsyncElasticsearchBase(
        index=VIDEO_INDEX, is_from_setting_if_none=True
    ) as crud:
        field_names = list(await crud.get_field_names())
        field_names.sort()
    return field_names
