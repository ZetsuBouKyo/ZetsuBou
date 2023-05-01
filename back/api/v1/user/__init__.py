from typing import List

from back.db.crud import CrudUser, CrudUserFrontSetting, CrudUserGroup
from back.db.model import (
    Group,
    ScopeEnum,
    UserCreate,
    UserCreated,
    UserFrontSetting,
    UserFrontSettingUpdateByUserId,
    UserGroupCreate,
    UserUpdate,
)
from back.dependency.security import api_security
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .elastic_query import router as elastic_query
from .quest import router as quest

router = APIRouter()


@router.post(
    "",
    response_model=UserCreated,
    dependencies=[api_security([ScopeEnum.user_post.name])],
)
async def post_user(user: UserCreate) -> UserCreated:
    return await CrudUser.create(user)


@router.get("/{user_id}", dependencies=[api_security([ScopeEnum.user_get.name])])
async def get_user_by_id(user_id: int):
    return await CrudUser.get_row_by_id(user_id)


@router.put("/{user_id}", dependencies=[api_security([ScopeEnum.user_put.name])])
async def put_user_by_id(user_id: int, user: UserUpdate):
    if user_id != user.id:
        return JSONResponse(
            status_code=409, content={"detail": "Conflict between user_id and user.id"}
        )
    return await CrudUser.update_by_id(user)


@router.delete("/{user_id}", dependencies=[api_security([ScopeEnum.user_delete.name])])
async def delete_user_by_id(user_id: int):
    return await CrudUser.delete_by_id(user_id)


@router.get(
    "/{user_id}/groups",
    response_model=List[Group],
    dependencies=[api_security([ScopeEnum.user_groups_get.name])],
)
async def get_user_groups_by_id(user_id: int) -> List[Group]:
    return await CrudUser.get_groups_by_id(user_id)


@router.post(
    "/{user_id}/groups", dependencies=[api_security([ScopeEnum.user_groups_post.name])]
)
async def post_user_groups_by_id(user_id: int, group_ids: List[int]):
    user_groups = []
    for group_id in group_ids:
        user_groups.append(UserGroupCreate(user_id=user_id, group_id=group_id))
    return await CrudUserGroup.batch_create(user_groups)


@router.get(
    "/{user_id}/front-setting",
    response_model=UserFrontSetting,
    dependencies=[api_security([ScopeEnum.user_front_setting_get.name])],
)
async def get_user_front_setting(user_id: int):
    return await CrudUserFrontSetting.get_row_by_user_id(user_id)


@router.put(
    "/{user_id}/front-setting",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_front_setting_put.name])],
)
async def put_user_front_setting(
    user_id: int, user_front_setting: UserFrontSettingUpdateByUserId
) -> bool:
    if user_id != user_front_setting.user_id:
        return JSONResponse(
            status_code=409, content={"detail": "Conflict between user_id and user.id"}
        )
    return await CrudUserFrontSetting.update_by_user_id(user_front_setting)


router.include_router(elastic_query, tags=["User Elastic Query"])
router.include_router(quest)
