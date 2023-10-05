from typing import List

from fastapi import APIRouter, Depends

from back.db.crud import CrudUser
from back.db.model import User, UserWithGroup
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(prefix="", tags=["Users"])


@router.get(
    "/total-users",
    response_model=int,
    dependencies=[api_security([ScopeEnum.users_total_get.value])],
)
async def count_total_users() -> int:
    return await CrudUser.count_total()


@router.get(
    "/users",
    response_model=List[User],
    dependencies=[api_security([ScopeEnum.users_get.value])],
)
async def get_users(
    pagination: Pagination = Depends(get_pagination),
) -> List[User]:
    return await CrudUser.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/users/with-groups",
    response_model=List[UserWithGroup],
    dependencies=[api_security([ScopeEnum.users_get.value])],
)
async def get_users_with_groups(
    pagination: Pagination = Depends(get_pagination),
) -> List[UserWithGroup]:
    return await CrudUser.get_rows_with_group_id_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )
