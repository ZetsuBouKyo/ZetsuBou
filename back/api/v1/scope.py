from typing import List

from fastapi import APIRouter, Depends

from back.db.crud import CrudScope
from back.db.model import Scope
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(tags=["Scope"])


@router.get(
    "/scopes",
    response_model=List[Scope],
    dependencies=[api_security([ScopeEnum.scopes_get.value])],
)
async def get_scopes(pagination: Pagination = Depends(get_pagination)) -> List[Scope]:
    return await CrudScope.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/scopes-startswith",
    response_model=List[Scope],
    dependencies=[api_security([ScopeEnum.scopes_startswith_get.value])],
)
async def startswith_scopes(
    name: str = "", pagination: Pagination = Depends(get_pagination)
) -> List[Scope]:
    return await CrudScope.startswith(
        name, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )
