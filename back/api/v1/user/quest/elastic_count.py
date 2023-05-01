from typing import List, Union

from back.db.crud import CrudUserElasticCountQuery, CrudUserElasticCountQuest
from back.db.model import (
    ScopeEnum,
    UserElasticCountQuest,
    UserElasticCountQuestCreate,
    UserElasticCountQuestCreated,
    UserElasticCountQuestUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


def verify_user_id(
    user_id: int, quest: Union[UserElasticCountQuestCreate, UserElasticCountQuestUpdate]
):
    if quest.user_id is None:
        quest.user_id = user_id
    elif user_id != quest.user_id:
        raise HTTPException(
            status_code=409, detail="Conflict between user_id and quest.user_id"
        )


async def verify_user_elastic_count_quest(
    user_id: int, quest: UserElasticCountQuestCreate
):
    query = await CrudUserElasticCountQuery.get_row_by_id_and_user_id(
        quest.numerator_id, user_id
    )
    if query is None:
        raise HTTPException(
            status_code=404, detail=f"numerator_id: {quest.numerator_id} not found"
        )
    query = await CrudUserElasticCountQuery.get_row_by_id_and_user_id(
        quest.denominator_id, user_id
    )
    if query is None:
        raise HTTPException(
            status_code=404, detail=f"denominator_id: {quest.denominator_id} not found"
        )


@router.get(
    "/{user_id}/total-elastic-count-quests",
    response_model=int,
    dependencies=[api_security([ScopeEnum.user_total_elastic_count_quests_get.name])],
)
async def count_total_user_elastic_count_quests(user_id: int) -> int:
    return await CrudUserElasticCountQuest.count_by_user_id(user_id)


@router.get(
    "/{user_id}/elastic-count-quest/{quest_id}",
    response_model=UserElasticCountQuest,
    dependencies=[api_security([ScopeEnum.user_elastic_count_quest_get.name])],
)
async def get_user_elastic_count_quest(
    user_id: int, quest_id: int
) -> UserElasticCountQuest:
    return await CrudUserElasticCountQuest.get_row_by_user_id_and_quest_id(
        user_id, quest_id
    )


@router.get(
    "/{user_id}/elastic-count-quests",
    response_model=List[UserElasticCountQuest],
    dependencies=[api_security([ScopeEnum.user_elastic_count_quests_get.name])],
)
async def get_user_elastic_count_quests(
    user_id: int, pagination: Pagination = Depends(get_pagination)
) -> List[UserElasticCountQuest]:
    return await CrudUserElasticCountQuest.get_rows_by_user_id_order_by_id(
        user_id, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/{user_id}/elastic-count-quest",
    response_model=UserElasticCountQuestCreated,
    dependencies=[
        Depends(verify_user_elastic_count_quest),
        api_security([ScopeEnum.user_elastic_count_quest_post.name]),
    ],
)
async def post_user_elastic_count_quest(
    user_id: int, quest: UserElasticCountQuestCreate
) -> UserElasticCountQuestCreated:
    verify_user_id(user_id, quest)
    return await CrudUserElasticCountQuest.create(quest)


@router.put(
    "/{user_id}/elastic-count-quest",
    dependencies=[
        Depends(verify_user_elastic_count_quest),
        api_security([ScopeEnum.user_elastic_count_quest_put.name]),
    ],
)
async def put_user_elastic_count_quest(
    user_id: int, quest: UserElasticCountQuestUpdate
):
    verify_user_id(user_id, quest)
    return await CrudUserElasticCountQuest.update_by_id(quest)


@router.delete(
    "/{user_id}/elastic-count-quest/{quest_id}",
    dependencies=[api_security([ScopeEnum.user_elastic_count_quest_delete.name])],
)
async def delete_user_elastic_count_quest(user_id: int, quest_id: int):
    return await CrudUserElasticCountQuest.delete_by_id_and_user_id(quest_id, user_id)
