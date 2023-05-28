from typing import List

from back.db.crud import CrudUserQuestCategory
from back.db.model import ScopeEnum, UserQuestCategory
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/user-quest-categories",
    response_model=List[UserQuestCategory],
    dependencies=[api_security([ScopeEnum.setting_user_quest_categories_get.name])],
)
async def get_user_quest_categories(
    pagination: Pagination = Depends(get_pagination),
) -> List[UserQuestCategory]:
    return await CrudUserQuestCategory.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/user-quest-category/{category_id}",
    response_model=UserQuestCategory,
    dependencies=[api_security([ScopeEnum.setting_user_quest_category_get.name])],
)
async def get_user_quest_category(category_id: int) -> UserQuestCategory:
    return await CrudUserQuestCategory.get_row_by_id(category_id)
