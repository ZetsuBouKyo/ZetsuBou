from typing import List

from fastapi import APIRouter

from back.db.crud import CrudUser
from back.db.model import User, UserWithGroup
from back.dependency.security import api_security
from back.model.scope import ScopeEnum

router = APIRouter(prefix="", tags=["Users"])


@router.get(
    "/total-users",
    response_model=int,
    dependencies=[api_security([ScopeEnum.users_total_get.name])],
)
async def count_total_users() -> int:
    return await CrudUser.count_total()


@router.get(
    "/users",
    response_model=List[User],
    dependencies=[api_security([ScopeEnum.users_get.name])],
)
async def get_users(
    skip: int = 0, limit: int = 20, is_desc: bool = False
) -> List[User]:
    return await CrudUser.get_rows_order_by_id(skip=skip, limit=limit, is_desc=is_desc)


@router.get(
    "/users/with-groups",
    response_model=List[UserWithGroup],
    dependencies=[api_security([ScopeEnum.users_get.name])],
)
async def get_users_with_groups(
    skip: int = 0, limit: int = 20, is_desc: bool = False
) -> List[UserWithGroup]:
    return await CrudUser.get_rows_with_group_id_order_by_id(
        skip=skip, limit=limit, is_desc=is_desc
    )
