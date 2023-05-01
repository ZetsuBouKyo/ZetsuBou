from typing import List

from back.db.crud import CrudGroup
from back.db.model import (
    Group,
    GroupCreatedWithScopes,
    GroupCreateWithScopes,
    GroupUpdateWithScopes,
    GroupWithScopes,
    ScopeEnum,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/total-groups",
    response_model=int,
    dependencies=[api_security([ScopeEnum.total_groups_get.name])],
)
async def get_total_groups() -> int:
    return await CrudGroup.count_total()


@router.get(
    "/group",
    response_model=List[Group],
    dependencies=[api_security([ScopeEnum.groups_get.name])],
)
async def get_groups(pagination: Pagination = Depends(get_pagination)) -> List[Group]:
    return await CrudGroup.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/group",
    response_model=GroupCreatedWithScopes,
    dependencies=[api_security([ScopeEnum.group_post.name])],
)
async def post_group_with_scopes(
    group: GroupCreateWithScopes,
) -> GroupCreatedWithScopes:
    return await CrudGroup.create_with_scopes(group)


@router.put(
    "/group",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.group_put.name])],
)
async def put_group_with_scopes(group: GroupUpdateWithScopes) -> bool:
    return await CrudGroup.update_with_scopes(group)


@router.get(
    "/group/{group_id}",
    response_model=GroupWithScopes,
    dependencies=[api_security([ScopeEnum.group_get.name])],
)
async def get_group_with_scopes(group_id: int) -> GroupWithScopes:
    return await CrudGroup.get_row_with_scopes_by_id(group_id)


@router.delete(
    "/group/{group_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.group_delete.name])],
)
async def delete_group(group_id: int) -> bool:
    return await CrudGroup.delete_by_id(group_id)
