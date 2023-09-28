from typing import List

from fastapi import APIRouter, Depends

from back.db.crud import CrudGroup
from back.db.model import Group, GroupCreate, GroupCreated, GroupUpdate
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(tags=["Group"])


@router.get(
    "/total-groups",
    response_model=int,
    dependencies=[api_security([ScopeEnum.total_groups_get.name])],
)
async def get_total_groups() -> int:
    return await CrudGroup.count_total()


@router.get(
    "/groups",
    response_model=List[Group],
    dependencies=[api_security([ScopeEnum.groups_get.name])],
)
async def get_groups(pagination: Pagination = Depends(get_pagination)) -> List[Group]:
    return await CrudGroup.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/group",
    response_model=GroupCreated,
    dependencies=[api_security([ScopeEnum.group_post.name])],
)
async def post_group(group: GroupCreate) -> GroupCreated:
    return await CrudGroup.create(group)


@router.put(
    "/group",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.group_post.name])],
)
async def post_group(group: GroupUpdate) -> bool:
    return await CrudGroup.update_by_id(group)


@router.delete(
    "/group/{group_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.group_delete.name])],
)
async def delete_group(group_id: int) -> bool:
    return await CrudGroup.delete_by_id(group_id)
