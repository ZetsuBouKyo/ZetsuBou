from typing import List, Optional

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from back.db.crud import CrudUser, CrudUserFrontSettings, CrudUserGroup
from back.db.model import (
    Group,
    User,
    UserFrontSettings,
    UserFrontSettingsUpdateByUserId,
    UserUpdate,
    UserWithGroups,
    UserWithGroupsCreate,
    UserWithGroupsCreated,
    UserWithGroupsUpdate,
)
from back.dependency.security import api_security
from back.model.scope import ScopeEnum

from .bookmark import router as bookmark
from .elastic_query import router as elastic_query
from .quest import router as quest

router = APIRouter(prefix="/user", tags=["User"])

post_user_openapi_examples = {
    "admin": {
        "summary": "An admin user",
        "description": "Create a user with `group_id=1`. By default, `group_id=1` is `admin`.",
        "value": {
            "name": "ZetsuBouKyo",
            "email": "zetsuboukyo@example.com",
            "password": "password",
            "group_ids": [1],
        },
    },
    "plain": {
        "summary": "A user without groups",
        "description": "Create a user without groups.",
        "value": {
            "name": "ZetsuBouKyo",
            "email": "zetsuboukyo@example.com",
            "password": "password",
            "group_ids": [],
        },
    },
}


@router.post(
    "",
    response_model=UserWithGroupsCreated,
    dependencies=[api_security([ScopeEnum.user_post.value])],
)
async def post_user(
    user: Annotated[
        UserWithGroupsCreate,
        Body(openapi_examples=post_user_openapi_examples),
    ]
) -> UserWithGroupsCreated:
    return await CrudUser.create_with_groups(user)


@router.get(
    "/{user_id}",
    response_model=Optional[User],
    dependencies=[api_security([ScopeEnum.user_get.value])],
)
async def get_user_by_id(user_id: int):
    return await CrudUser.get_row_by_id(user_id)


@router.get(
    "/{user_id}/with-groups",
    response_model=Optional[UserWithGroups],
    dependencies=[api_security([ScopeEnum.user_with_groups_get.value])],
)
async def get_user_with_groups_by_id(user_id: int) -> UserWithGroups:
    return await CrudUser.get_row_with_groups_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=User,
    dependencies=[api_security([ScopeEnum.user_put.value])],
)
async def put_user_by_id(user_id: int, user: UserUpdate):
    return await CrudUser.update_by_user(user_id, user)


@router.put(
    "/{user_id}/with-groups",
    response_model=UserWithGroups,
    dependencies=[api_security([ScopeEnum.user_with_groups_put.value])],
)
async def put_user_with_groups_by_id(user_id: int, user: UserWithGroupsUpdate):
    return await CrudUser.update_by_user_with_group(user_id, user)


@router.delete("/{user_id}", dependencies=[api_security([ScopeEnum.user_delete.value])])
async def delete_user_by_id(user_id: int):
    return await CrudUser.delete_by_id(user_id)


@router.get(
    "/{user_id}/groups",
    response_model=List[Group],
    dependencies=[api_security([ScopeEnum.user_groups_get.value])],
)
async def get_user_groups(user_id: int) -> List[Group]:
    return await CrudUser.get_groups_by_id(user_id)


@router.put(
    "/{user_id}/groups", dependencies=[api_security([ScopeEnum.user_groups_put.value])]
)
async def put_user_groups(user_id: int, group_ids: List[int]):
    return await CrudUserGroup.update(user_id, group_ids)


@router.put(
    "/{user_id}/front-settings",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_front_settings_put.value])],
)
async def put_user_front_settings(
    user_id: int, settings: UserFrontSettingsUpdateByUserId
) -> bool:
    if user_id != settings.user_id:
        return JSONResponse(
            status_code=409, content={"detail": "Conflict between user_id and user.id"}
        )
    return await CrudUserFrontSettings.update_by_user_id(settings)


@router.get(
    "/{user_id}/front-settings",
    response_model=UserFrontSettings,
    dependencies=[api_security([ScopeEnum.user_front_settings_get.value])],
)
async def get_user_front_settings(user_id: int):
    return await CrudUserFrontSettings.get_row_by_user_id(user_id)


router.include_router(elastic_query, tags=["User Elastic Query"])
router.include_router(bookmark)
router.include_router(quest)
