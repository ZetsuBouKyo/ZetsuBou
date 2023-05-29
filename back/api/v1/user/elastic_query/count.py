from typing import List

from back.db.crud import CrudUserElasticCountQuery
from back.db.model import (
    UserElasticCountQuery,
    UserElasticCountQueryCreate,
    UserElasticCountQueryCreated,
    UserElasticCountQueryUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum
from fastapi import APIRouter, Depends

from .dep import verify_user_id

router = APIRouter()


@router.get(
    "/{user_id}/elastic/total-count-queries",
    response_model=int,
    dependencies=[api_security([ScopeEnum.user_elastic_total_count_queries_get.name])],
)
async def count_total_user_elastic_count_queries(user_id: int) -> int:
    return await CrudUserElasticCountQuery.count_by_user_id(user_id)


@router.get(
    "/{user_id}/elastic/count-queries",
    response_model=List[UserElasticCountQuery],
    dependencies=[api_security([ScopeEnum.user_elastic_count_queries_get.name])],
)
async def get_user_elastic_count_queries(
    user_id: int, pagination: Pagination = Depends(get_pagination)
) -> List[UserElasticCountQuery]:
    return await CrudUserElasticCountQuery.get_rows_by_user_id_order_by_id(
        user_id, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/{user_id}/elastic/count-query/{query_id}",
    response_model=UserElasticCountQuery,
    dependencies=[api_security([ScopeEnum.user_elastic_count_query_get.name])],
)
async def get_user_elastic_count_query(
    user_id: int, query_id: int
) -> UserElasticCountQuery:
    return await CrudUserElasticCountQuery.get_row_by_id_and_user_id(query_id, user_id)


@router.post(
    "/{user_id}/elastic/count-query",
    response_model=UserElasticCountQueryCreated,
    dependencies=[api_security([ScopeEnum.user_elastic_count_query_post.name])],
)
async def post_user_elastic_count_query(
    user_id: int,
    query: UserElasticCountQueryCreate,
) -> UserElasticCountQueryCreated:
    verify_user_id(user_id, query)
    return await CrudUserElasticCountQuery.create(query)


@router.put(
    "/{user_id}/elastic/count-query",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_elastic_count_query_put.name])],
)
async def put_user_elastic_count_query(
    user_id: int, query: UserElasticCountQueryUpdate
) -> bool:
    verify_user_id(user_id, query)
    return await CrudUserElasticCountQuery.update_by_id(query)


@router.delete(
    "/{user_id}/elastic/count-query/{query_id}",
    dependencies=[api_security([ScopeEnum.user_elastic_count_query_delete.name])],
)
async def delete_user_elastic_count_query_by_id(user_id: int, query_id: int) -> bool:
    return await CrudUserElasticCountQuery.delete_by_id_and_user_id(query_id, user_id)
