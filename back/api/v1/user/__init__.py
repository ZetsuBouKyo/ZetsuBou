from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body
from fastapi.params import Path
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
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
from back.model.example import ExampleEnum
from back.model.scope import ScopeEnum
from back.utils import get_subset_dict

from .bookmark import router as bookmark
from .elastic_query import router as elastic_query
from .examples import param_path_user_id
from .quest import router as quest


def get_admin_user(*params: str) -> Dict[str, Any]:
    return get_subset_dict(
        *params,
        base={
            "name": ExampleEnum.USER_NAME.value,
            "email": ExampleEnum.USER_EMAIL.value,
            "password": ExampleEnum.PASSWORD.value,
            "new_password": ExampleEnum.NEW_PASSWORD.value,
            "group_ids": [1],
        }
    )


def get_user(*params: str) -> Dict[str, Any]:
    return get_subset_dict(
        *params,
        base={
            "name": ExampleEnum.USER_NAME.value,
            "email": ExampleEnum.USER_EMAIL.value,
            "password": ExampleEnum.PASSWORD.value,
            "new_password": ExampleEnum.NEW_PASSWORD.value,
            "group_ids": [],
        }
    )


router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "",
    response_model=UserWithGroupsCreated,
    dependencies=[api_security([ScopeEnum.user_post.value])],
)
async def post_user(
    user: Annotated[
        UserWithGroupsCreate,
        Body(
            examples=[
                get_admin_user("name", "email", "password", "group_ids"),
                get_user("name", "email", "password", "group_ids"),
            ],
            openapi_examples={
                "admin": {
                    "summary": "An admin user",
                    "description": "Create a user with `group_id=1`. By default, `group_id=1` is `admin`.",
                    "value": get_admin_user("name", "email", "password", "group_ids"),
                },
                "plain": {
                    "summary": "A user without groups",
                    "description": "Create a user without groups.",
                    "value": get_user("name", "email", "password", "group_ids"),
                },
            },
        ),
    ]
) -> UserWithGroupsCreated:
    return await CrudUser.create_with_groups(user)


@router.get(
    "/{user_id}",
    response_model=Optional[User],
    dependencies=[api_security([ScopeEnum.user_get.value])],
)
async def get_user_by_id(user_id: PositiveInt = param_path_user_id):
    return await CrudUser.get_row_by_id(user_id)


@router.get(
    "/{user_id}/with-groups",
    response_model=Optional[UserWithGroups],
    dependencies=[api_security([ScopeEnum.user_with_groups_get.value])],
)
async def get_user_with_groups_by_id(
    user_id: PositiveInt = param_path_user_id,
) -> UserWithGroups:
    return await CrudUser.get_row_with_groups_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=User,
    dependencies=[api_security([ScopeEnum.user_put.value])],
)
async def put_user_by_id(
    user: Annotated[
        UserUpdate,
        Body(
            examples=[
                get_admin_user("name", "email", "password", "new_password"),
                get_user("name", "email", "password", "new_password"),
            ],
            openapi_examples={
                "password": {
                    "summary": "Update password",
                    "description": "Update password.",
                    "value": get_admin_user("email", "password", "new_password"),
                },
                "name": {
                    "summary": "Update user name",
                    "description": "Update user name.",
                    "value": get_user("name", "email", "password"),
                },
            },
        ),
    ],
    user_id: PositiveInt = param_path_user_id,
):
    return await CrudUser.update_by_user(user_id, user)


@router.put(
    "/{user_id}/with-groups",
    response_model=UserWithGroups,
    dependencies=[api_security([ScopeEnum.user_with_groups_put.value])],
)
async def put_user_with_groups_by_id(
    user: Annotated[
        UserWithGroupsUpdate,
        Body(
            examples=[
                get_admin_user(
                    "name", "email", "password", "new_password", "group_ids"
                ),
                get_user("name", "email", "password", "new_password", "group_ids"),
            ],
            openapi_examples={
                "password": {
                    "summary": "Update password",
                    "description": "Update password.",
                    "value": get_admin_user(
                        "email", "password", "new_password", "group_ids"
                    ),
                },
                "name": {
                    "summary": "Update user name",
                    "description": "Update user name.",
                    "value": get_user("name", "email", "password", "group_ids"),
                },
            },
        ),
    ],
    user_id: PositiveInt = param_path_user_id,
):
    return await CrudUser.update_by_user_with_group(user_id, user)


@router.delete("/{user_id}", dependencies=[api_security([ScopeEnum.user_delete.value])])
async def delete_user_by_id(user_id: PositiveInt = param_path_user_id):
    return await CrudUser.delete_by_id(user_id)


@router.get(
    "/{user_id}/groups",
    response_model=List[Group],
    dependencies=[api_security([ScopeEnum.user_groups_get.value])],
)
async def get_user_groups(user_id: PositiveInt = param_path_user_id) -> List[Group]:
    return await CrudUser.get_groups_by_id(user_id)


@router.put(
    "/{user_id}/groups", dependencies=[api_security([ScopeEnum.user_groups_put.value])]
)
async def put_user_groups(
    group_ids: Annotated[
        List[int],
        Body(
            examples=[[], [1], [1, 2]],
            openapi_examples={
                "none": {
                    "summary": "No group IDs",
                    "description": "No group IDs.",
                    "value": [],
                },
                "single": {
                    "summary": "Single group ID",
                    "description": "Single group ID.",
                    "value": [1],
                },
                "multiple": {
                    "summary": "Multiple group IDs",
                    "description": "Multiple group IDs.",
                    "value": [1, 2],
                },
            },
        ),
    ],
    user_id: PositiveInt = param_path_user_id,
):
    return await CrudUserGroup.update(user_id, group_ids)


@router.put(
    "/{user_id}/front-settings",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_front_settings_put.value])],
)
async def put_user_front_settings(
    settings: Annotated[
        UserFrontSettingsUpdateByUserId,
        Body(
            examples=[
                {
                    "user_id": ExampleEnum.USER_ID.value,
                    "gallery_preview_size": ExampleEnum.GALLERY_PREVIEW_SIZE.value,
                },
                {
                    "user_id": ExampleEnum.USER_ID.value,
                    "gallery_image_auto_play_time_interval": ExampleEnum.GALLERY_IMAGE_AUTO_PLAY_TIME_INTERVAL.value,
                },
                {
                    "user_id": ExampleEnum.USER_ID.value,
                    "gallery_preview_size": ExampleEnum.GALLERY_PREVIEW_SIZE.value,
                    "gallery_image_auto_play_time_interval": ExampleEnum.GALLERY_IMAGE_AUTO_PLAY_TIME_INTERVAL.value,
                    "gallery_image_preview_size": ExampleEnum.GALLERY_IMAGE_PREVIEW_SIZE.value,
                    "video_preview_size": ExampleEnum.VIDEO_PREVIEW_SIZE.value,
                },
            ],
            openapi_examples={
                "single": {
                    "summary": "Single setting",
                    "description": "Single setting.",
                    "value": {
                        "user_id": ExampleEnum.USER_ID.value,
                        "gallery_preview_size": ExampleEnum.GALLERY_PREVIEW_SIZE.value,
                    },
                },
                "multiple": {
                    "summary": "Multiple settings",
                    "description": "Multiple settings.",
                    "value": {
                        "user_id": ExampleEnum.USER_ID.value,
                        "gallery_preview_size": ExampleEnum.GALLERY_PREVIEW_SIZE.value,
                        "gallery_image_auto_play_time_interval": ExampleEnum.GALLERY_IMAGE_AUTO_PLAY_TIME_INTERVAL.value,
                        "gallery_image_preview_size": ExampleEnum.GALLERY_IMAGE_PREVIEW_SIZE.value,
                        "video_preview_size": ExampleEnum.VIDEO_PREVIEW_SIZE.value,
                    },
                },
            },
        ),
    ],
    user_id: PositiveInt = param_path_user_id,
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
async def get_user_front_settings(user_id: PositiveInt = param_path_user_id):
    return await CrudUserFrontSettings.get_row_by_user_id(user_id)


router.include_router(elastic_query, tags=["User Elastic Query"])
router.include_router(bookmark)
router.include_router(quest)
