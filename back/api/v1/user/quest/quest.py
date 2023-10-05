from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException

from back.api.model.user.quest import CurrentQuestProgress
from back.crud.user_quest import CrudElasticCount
from back.db.crud import CrudUserElasticCountQuest, CrudUserQuest, CrudUserQuestCategory
from back.db.model import (
    UserQuest,
    UserQuestCategoryEnum,
    UserQuestCreate,
    UserQuestCreated,
    UserQuestUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(tags=["User Quest"])


def verify_user_id(user_id: int, quest: Union[UserQuestCreated, UserQuestUpdate]):
    if quest.user_id is None:
        quest.user_id = user_id
    elif user_id != quest.user_id:
        raise HTTPException(
            status_code=409, detail="Conflict between user_id and quest.user_id"
        )


async def verify_quest(user_id: int, quest: UserQuestCreate):
    category = await CrudUserQuestCategory.get_row_by_id(quest.category_id)
    if category is None:
        raise HTTPException(
            status_code=404, detail=f"category_id: {quest.category_id} not found"
        )
    if category.name == UserQuestCategoryEnum.ELASTIC_COUNT_QUEST.value:
        es_quest = await CrudUserElasticCountQuest.get_row_by_id(quest.quest_id)
        if es_quest is None:
            raise HTTPException(
                status_code=404, detail=f"ElasticCountQuest: {quest.quest_id} not found"
            )
        elif es_quest.user_id != user_id:
            raise HTTPException(
                status_code=409,
                detail="Conflict between user_id and user_id of quest.quest_id",
            )
        return
    raise HTTPException(status_code=404, detail="category not found")


async def get_elastic_count_quest_progress(quest_id: int) -> CurrentQuestProgress:
    quest = await CrudUserElasticCountQuest.get_row_by_id(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail=f"Quest Id: {quest_id} not found")

    numerator_count = await CrudElasticCount.count(quest.numerator_id)
    denominator_count = await CrudElasticCount.count(quest.denominator_id)

    return CurrentQuestProgress(
        numerator=numerator_count, denominator=denominator_count
    )


@router.get(
    "/{user_id}/current-quest-progress",
    response_model=CurrentQuestProgress,
    dependencies=[api_security([ScopeEnum.user_current_quest_progress_get.value])],
)
async def get_user_current_quest_progress(user_id: int) -> CurrentQuestProgress:
    quests = await CrudUserQuest.get_top_priority(user_id)
    if not quests:
        return CurrentQuestProgress()

    quest = quests[0]
    category = await CrudUserQuestCategory.get_row_by_id(quest.category_id)

    if not category:
        raise HTTPException(
            status_code=404, detail=f"Category Id: {quest.category_id} not found"
        )

    if category.name == UserQuestCategoryEnum.ELASTIC_COUNT_QUEST.value:
        return await get_elastic_count_quest_progress(quest.quest_id)

    raise HTTPException(status_code=404, detail=f"Category: {category.name} not found")


@router.get(
    "/{user_id}/total-quests",
    response_model=int,
    dependencies=[api_security([ScopeEnum.user_total_quests_get.value])],
)
async def count_total_user_quests(user_id: int) -> int:
    return await CrudUserQuest.count_by_user_id(user_id)


@router.get(
    "/{user_id}/quests",
    response_model=List[UserQuest],
    dependencies=[api_security([ScopeEnum.user_quests_get.value])],
)
async def get_user_quests(
    user_id: int, pagination: Pagination = Depends(get_pagination)
) -> List[UserQuest]:
    return await CrudUserQuest.get_rows_by_user_id_order_by_id(
        user_id, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/{user_id}/quest",
    response_model=UserQuestCreated,
    dependencies=[
        Depends(verify_quest),
        api_security([ScopeEnum.user_quest_post.value]),
    ],
)
async def post_user_quest(user_id: int, quest: UserQuestCreate) -> UserQuestCreated:
    verify_user_id(user_id, quest)
    return await CrudUserQuest.create(quest)


@router.put(
    "/{user_id}/quest",
    dependencies=[
        Depends(verify_quest),
        api_security([ScopeEnum.user_quest_put.value]),
    ],
)
async def put_user_quest(user_id: int, quest: UserQuestUpdate):
    verify_user_id(user_id, quest)
    return await CrudUserQuest.update_by_id(quest)


@router.delete(
    "/{user_id}/quest/{quest_id}",
    dependencies=[api_security([ScopeEnum.user_quest_delete.value])],
)
async def delete_user_quest(user_id: int, quest_id: int):
    return await CrudUserQuest.delete_by_id_and_user_id(quest_id, user_id)
