from typing import List

from back.db.crud import CrudUser
from back.db.model import User
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=List[User],
    dependencies=[api_security([ScopeEnum.users_get.name])],
)
async def get_users(
    skip: int = 0, limit: int = 20, is_desc: bool = False
) -> List[User]:
    return await CrudUser.get_rows_order_by_id(skip=skip, limit=limit, is_desc=is_desc)
