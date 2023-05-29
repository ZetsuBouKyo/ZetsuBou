import json
from urllib.parse import unquote

from back.crud.async_gallery import CrudAsyncElasticsearchGallery
from back.db.crud import CrudUserElasticSearchQuery
from back.db.model import ScopeEnum
from back.dependency.security import Token, api_security, extract_token
from back.model.elasticsearch import AnalyzerEnum, Count, QueryBoolean
from back.model.gallery import Galleries, GalleryOrderedFieldEnum
from back.settings import setting
from fastapi import APIRouter, Body, Depends, Request

from ...model.gallery import CustomQuery, query_examples
from ..utils import get_tags_and_labels_by_query_params

router = APIRouter()

host = setting.app_host
elastic_size = setting.elastic_size


def get_body(query: CustomQuery):
    body = query.body
    body = unquote(json.dumps(body))
    body = json.loads(body)
    return body


@router.get(
    "/count/{field}/{value}",
    response_model=Count,
    dependencies=[api_security([ScopeEnum.gallery_query_count_field_value_get.name])],
)
async def get_count_field(field: str, value: str):
    body = {"query": {"terms": {field: [value]}}}
    crud = CrudAsyncElasticsearchGallery(is_from_setting_if_none=True)
    return await crud.count(body)


@router.post(
    "/count",
    response_model=Count,
    dependencies=[api_security([ScopeEnum.gallery_query_count_post.name])],
)
async def post_count(query: CustomQuery = Body(..., examples=query_examples)) -> Count:
    body = get_body(query)
    crud = CrudAsyncElasticsearchGallery(is_from_setting_if_none=True)
    return await crud.count(body)


@router.get(
    "/random",
    response_model=Galleries,
    dependencies=[api_security([ScopeEnum.gallery_query_random_get.name])],
)
async def get_random(
    analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    seed: int = 1048596,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = 0,
    size: int = elastic_size,
    boolean: QueryBoolean = QueryBoolean.SHOULD,
) -> Galleries:
    keywords = unquote(keywords)
    crud = CrudAsyncElasticsearchGallery(
        size=size, analyzer=analyzer, is_from_setting_if_none=True
    )
    return await crud.random(
        page, keywords, fuzziness=fuzziness, boolean=boolean, seed=seed
    )


@router.post(
    "/custom-search",
    response_model=dict,
    dependencies=[api_security([ScopeEnum.gallery_query_custom_search_post.name])],
)
async def post_custom_search(query: CustomQuery = Body(..., examples=query_examples)):
    body = get_body(query)
    crud = CrudAsyncElasticsearchGallery(is_from_setting_if_none=True)
    return await crud.custom(body)


@router.get(
    "/advanced-search",
    response_model=Galleries,
    dependencies=[api_security([ScopeEnum.gallery_query_advanced_search_get.name])],
)
async def get_advanced_search(
    request: Request,
    page: int = 1,
    size: int = elastic_size,
    keywords: str = None,
    keywords_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    keywords_fuzziness: int = 0,
    keywords_bool: QueryBoolean = QueryBoolean.SHOULD,
    name: str = None,
    name_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    name_fuzziness: int = 0,
    name_bool: QueryBoolean = QueryBoolean.SHOULD,
    raw_name: str = None,
    raw_name_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    raw_name_fuzziness: int = 0,
    raw_name_bool: QueryBoolean = QueryBoolean.SHOULD,
    src: str = None,
    src_analyzer: AnalyzerEnum = AnalyzerEnum.URL,
    src_fuzziness: int = 0,
    src_bool: QueryBoolean = QueryBoolean.SHOULD,
    path: str = None,
    path_analyzer: AnalyzerEnum = AnalyzerEnum.URL,
    path_fuzziness: int = 0,
    path_bool: QueryBoolean = QueryBoolean.SHOULD,
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
    crud = CrudAsyncElasticsearchGallery(size=size)

    return await crud.advanced_search(
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


@router.get(
    "/search",
    response_model=Galleries,
    dependencies=[api_security([ScopeEnum.gallery_query_search_get.name])],
)
async def get_search(
    analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    token: Token = Depends(extract_token),
    query_id: int = None,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = 0,
    size: int = elastic_size,
    boolean: QueryBoolean = QueryBoolean.SHOULD,
) -> Galleries:
    user_id = token.sub
    keywords = unquote(keywords)

    crud = CrudAsyncElasticsearchGallery(size=size, analyzer=analyzer)
    if query_id is not None:
        user_es_query = await CrudUserElasticSearchQuery.get_row_by_id_and_user_id(
            query_id, user_id
        )
        query = json.loads(user_es_query.query)
        body = query.get("body", None)
        if body is None:
            return []
        return await crud.match_by_query(body, page)

    return await crud.match(page, keywords, fuzziness=fuzziness, boolean=boolean)
