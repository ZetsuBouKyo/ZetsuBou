from typing import List, Optional

from fastapi import APIRouter, Depends

from back.db.crud import CrudGroup
from back.db.model import (
    Group,
    GroupWithScopeIdsSafeCreate,
    GroupWithScopeIdsUpdate,
    GroupWithScopes,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(tags=["Group"])


@router.get(
    "/total-groups",
    response_model=int,
    dependencies=[api_security([ScopeEnum.total_groups_get.value])],
)
async def get_total_groups() -> int:
    return await CrudGroup.count_total()


@router.get(
    "/groups",
    response_model=List[Group],
    dependencies=[api_security([ScopeEnum.groups_get.value])],
)
async def get_groups(pagination: Pagination = Depends(get_pagination)) -> List[Group]:
    return await CrudGroup.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/group-with-scopes/{group_id}",
    response_model=Optional[GroupWithScopes],
    dependencies=[api_security([ScopeEnum.group_with_scopes_get.value])],
)
async def get_group_with_scopes(group_id: int) -> Optional[GroupWithScopes]:
    return await CrudGroup.get_row_with_scopes_by_id(group_id)


@router.post(
    "/group-with-scope-ids",
    response_model=GroupWithScopes,
    dependencies=[api_security([ScopeEnum.group_with_scope_ids_post.value])],
)
async def post_group_with_scope_ids(
    group: GroupWithScopeIdsSafeCreate,
) -> GroupWithScopes:
    return await CrudGroup.safe_create_with_scope_ids(group)


@router.put(
    "/group-with-scope-ids",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.group_with_scope_ids_put.value])],
)
async def put_group_with_scope_ids(group: GroupWithScopeIdsUpdate) -> bool:
    return await CrudGroup.update_with_scope_ids_by_id(group)


@router.delete(
    "/group/{group_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.group_delete.value])],
)
async def delete_group(group_id: int) -> bool:
    return await CrudGroup.delete_by_id(group_id)
