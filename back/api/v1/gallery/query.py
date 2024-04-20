import json
from urllib.parse import unquote

from fastapi import APIRouter, Body, Depends, Request

from back.api.model.gallery import CustomQuery, query_examples
from back.api.v1.utils import get_tags_and_labels_by_query_params
from back.crud.async_gallery import CrudAsyncElasticsearchGallery
from back.db.crud import CrudUserElasticSearchQuery
from back.dependency.security import Token, api_security, extract_token
from back.model.elasticsearch import AnalyzerEnum, Count, QueryBooleanEnum
from back.model.gallery import Galleries, GalleryOrderedFieldEnum
from back.model.scope import ScopeEnum
from back.settings import setting

router = APIRouter(tags=["Gallery Query"])

ELASTIC_SIZE = setting.elastic_size


def get_body(query: CustomQuery):
    body = query.body
    body = unquote(json.dumps(body))
    body = json.loads(body)
    return body


@router.get(
    "/count/{field}/{value}",
    response_model=Count,
    dependencies=[api_security([ScopeEnum.gallery_count_field_value_get.value])],
)
async def get_count_field(field: str, value: str):
    body = {"query": {"terms": {field: [value]}}}
    async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
        count = await crud.count(body)
    return count


@router.post(
    "/count",
    response_model=Count,
    dependencies=[api_security([ScopeEnum.gallery_count_post.value])],
)
async def post_count(query: CustomQuery = Body(..., examples=query_examples)) -> Count:
    body = get_body(query)
    async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
        count = await crud.count(body)
    return count


@router.get(
    "/random",
    response_model=Galleries,
    dependencies=[api_security([ScopeEnum.gallery_random_get.value])],
)
async def get_random(
    analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    seed: int = 1048596,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = 0,
    size: int = ELASTIC_SIZE,
    boolean: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
) -> Galleries:
    keywords = unquote(keywords)
    async with CrudAsyncElasticsearchGallery(
        size=size, analyzer=analyzer, is_from_setting_if_none=True
    ) as crud:
        docs = await crud.random(
            page, keywords, fuzziness=fuzziness, boolean=boolean, seed=seed
        )
    return docs


@router.post(
    "/custom-search",
    response_model=dict,
    dependencies=[api_security([ScopeEnum.gallery_custom_search_post.value])],
)
async def post_custom_search(query: CustomQuery = Body(..., examples=query_examples)):
    body = get_body(query)
    async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
        docs = await crud.custom(body)
    return docs


@router.get(
    "/advanced-search",
    response_model=Galleries,
    dependencies=[api_security([ScopeEnum.gallery_advanced_search_get.value])],
)
async def get_advanced_search(
    request: Request,
    page: int = 1,
    size: int = ELASTIC_SIZE,
    keywords: str = None,
    keywords_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    keywords_fuzziness: int = 0,
    keywords_bool: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
    name: str = None,
    name_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    name_fuzziness: int = 0,
    name_bool: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
    raw_name: str = None,
    raw_name_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    raw_name_fuzziness: int = 0,
    raw_name_bool: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
    src: str = None,
    src_analyzer: AnalyzerEnum = AnalyzerEnum.URL,
    src_fuzziness: int = 0,
    src_bool: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
    path: str = None,
    path_analyzer: AnalyzerEnum = AnalyzerEnum.URL,
    path_fuzziness: int = 0,
    path_bool: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
    category: str = None,
    uploader: str = None,
    rating_gte: int = None,
    rating_lte: int = None,
    tag_field_1: str = None,
    tag_value_1: str = None,
    label_1: str = None,
    order_by: GalleryOrderedFieldEnum = None,
    is_desc: bool = True,
) -> Galleries:
    tags, labels = get_tags_and_labels_by_query_params(request)

    if keywords is not None:
        keywords = unquote(keywords)
    if name is not None:
        name = unquote(name)
    if raw_name is not None:
        raw_name = unquote(raw_name)
    async with CrudAsyncElasticsearchGallery(
        size=size, is_from_setting_if_none=True
    ) as crud:
        docs = await crud.advanced_search(
            page=page,
            keywords=keywords,
            keywords_analyzer=keywords_analyzer,
            keywords_fuzziness=keywords_fuzziness,
            keywords_bool=keywords_bool,
            name=name,
            name_analyzer=name_analyzer,
            name_fuzziness=name_fuzziness,
            name_bool=name_bool,
            raw_name=raw_name,
            raw_name_analyzer=raw_name_analyzer,
            raw_name_fuzziness=raw_name_fuzziness,
            raw_name_bool=raw_name_bool,
            src=src,
            src_analyzer=src_analyzer,
            src_fuzziness=src_fuzziness,
            src_bool=src_bool,
            path=path,
            path_analyzer=path_analyzer,
            path_fuzziness=path_fuzziness,
            path_bool=path_bool,
            category=category,
            uploader=uploader,
            rating_gte=rating_gte,
            rating_lte=rating_lte,
            order_by=order_by,
            is_desc=is_desc,
            labels=labels,
            tags=tags,
        )
    return docs


@router.get(
    "/search",
    response_model=Galleries,
    dependencies=[api_security([ScopeEnum.gallery_search_get.value])],
)
async def get_search(
    analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    token: Token = Depends(extract_token),
    query_id: int = None,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = 0,
    size: int = ELASTIC_SIZE,
    boolean: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
) -> Galleries:
    user_id = token.sub
    keywords = unquote(keywords)

    async with CrudAsyncElasticsearchGallery(
        size=size, analyzer=analyzer, is_from_setting_if_none=True
    ) as crud:
        if query_id is not None:
            user_es_query = await CrudUserElasticSearchQuery.get_row_by_id_and_user_id(
                query_id, user_id
            )
            query = json.loads(user_es_query.query)
            body = query.get("body", None)
            if body is None:
                return []
            docs = await crud.match_by_query(body, page)
        else:
            docs = await crud.match(
                page, keywords, fuzziness=fuzziness, boolean=boolean
            )
    return docs
