from typing import List

from back.db.crud import CrudUserElasticSearchQuery
from back.db.model import (
    ScopeEnum,
    UserElasticSearchQuery,
    UserElasticSearchQueryCreate,
    UserElasticSearchQueryCreated,
    UserElasticSearchQueryUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from fastapi import APIRouter, Depends

from .dep import verify_user_id

router = APIRouter()


@router.get(
    "/{user_id}/elastic/total-search-queries",
    response_model=int,
    dependencies=[api_security([ScopeEnum.user_elastic_total_search_queries_get.name])],
)
async def count_total_user_elastic_search_queries(user_id: int) -> int:
    return await CrudUserElasticSearchQuery.count_by_user_id(user_id)


@router.get(
    "/{user_id}/elastic/search-queries",
    response_model=List[UserElasticSearchQuery],
    dependencies=[api_security([ScopeEnum.user_elastic_search_queries_get.name])],
)
async def get_user_elastic_search_queries(
    user_id: int, pagination: Pagination = Depends(get_pagination)
) -> List[UserElasticSearchQuery]:
    return await CrudUserElasticSearchQuery.get_rows_by_user_id_order_by_id(
        user_id, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/{user_id}/elastic/search-query",
    response_model=UserElasticSearchQuery,
    dependencies=[api_security([ScopeEnum.user_elastic_search_query_get.name])],
)
async def get_user_elastic_search_query(
    user_id: int, query_id: int
) -> UserElasticSearchQuery:
    return await CrudUserElasticSearchQuery.get_row_by_id_and_user_id(query_id, user_id)


@router.post(
    "/{user_id}/elastic/search-query",
    response_model=UserElasticSearchQueryCreated,
    dependencies=[api_security([ScopeEnum.user_elastic_search_query_post.name])],
)
async def post_user_elastic_search_query(
    user_id: int, query: UserElasticSearchQueryCreate
) -> UserElasticSearchQueryCreated:
    verify_user_id(user_id, query)
    return await CrudUserElasticSearchQuery.create(query)


@router.put(
    "/{user_id}/elastic/search-query",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_elastic_search_query_put.name])],
)
async def put_user_elastic_search_query(
    user_id: int, query: UserElasticSearchQueryUpdate
) -> bool:
    verify_user_id(user_id, query)
    return await CrudUserElasticSearchQuery.update_by_id(query)


@router.delete(
    "/{user_id}/elastic/search-query/{query_id}",
    dependencies=[api_security([ScopeEnum.user_elastic_search_query_delete.name])],
)
async def delete_user_elastic_search_query_by_id(user_id: int, query_id: int) -> bool:
    return await CrudUserElasticSearchQuery.delete_by_id_and_user_id(query_id, user_id)
