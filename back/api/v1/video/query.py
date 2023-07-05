import json
from urllib.parse import unquote

from fastapi import APIRouter, Depends, Request

from back.crud.async_video import CrudAsyncElasticsearchVideo
from back.db.crud import CrudUserElasticSearchQuery
from back.dependency.security import Token, api_security, extract_token
from back.model.elasticsearch import AnalyzerEnum, QueryBooleanEnum
from back.model.scope import ScopeEnum
from back.model.video import VideoOrderedFieldEnum, Videos
from back.settings import setting

from ..utils import get_tags_and_labels_by_query_params

router = APIRouter()

ELASTIC_SIZE = setting.elastic_size


@router.get(
    "/random",
    response_model=Videos,
    dependencies=[api_security([ScopeEnum.video_random_get.name])],
)
async def get_random(
    analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    seed: int = 1048596,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = 0,
    size: int = ELASTIC_SIZE,
    boolean: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
) -> Videos:
    keywords = unquote(keywords)
    crud = CrudAsyncElasticsearchVideo(
        size=size, analyzer=analyzer, is_from_setting_if_none=True
    )
    return await crud.random(
        page, keywords, fuzziness=fuzziness, boolean=boolean, seed=seed
    )


@router.get(
    "/advanced-search",
    response_model=Videos,
    dependencies=[api_security([ScopeEnum.video_advanced_search_get.name])],
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
    other_names: str = None,
    other_names_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    other_names_fuzziness: int = 0,
    other_names_bool: QueryBooleanEnum = QueryBooleanEnum.SHOULD,
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
    height_gte: int = None,
    height_lte: int = None,
    width_gte: int = None,
    width_lte: int = None,
    duration_gte: int = None,
    duration_lte: int = None,
    tag_field_1: str = None,
    tag_value_1: str = None,
    label_1: str = None,
    order_by: VideoOrderedFieldEnum = None,
    is_desc: bool = True,
) -> Videos:
    tags, labels = get_tags_and_labels_by_query_params(request)

    if keywords is not None:
        keywords = unquote(keywords)
    if name is not None:
        name = unquote(name)
    if other_names is not None:
        other_names = unquote(other_names)
    crud = CrudAsyncElasticsearchVideo(size=size)

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
        other_names=other_names,
        other_names_analyzer=other_names_analyzer,
        other_names_fuzziness=other_names_fuzziness,
        other_names_bool=other_names_bool,
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
        height_gte=height_gte,
        height_lte=height_lte,
        width_gte=width_gte,
        width_lte=width_lte,
        duration_gte=duration_gte,
        duration_lte=duration_lte,
        order_by=order_by,
        is_desc=is_desc,
        labels=labels,
        tags=tags,
    )


@router.get(
    "/search",
    response_model=Videos,
    dependencies=[api_security([ScopeEnum.video_search_get.name])],
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
) -> Videos:
    user_id = token.sub
    keywords = unquote(keywords)

    crud = CrudAsyncElasticsearchVideo(size=size, analyzer=analyzer)
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
