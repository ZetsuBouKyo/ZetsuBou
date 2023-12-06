from typing import List

from fastapi import APIRouter, Depends

from back.db.crud import CrudSettingFrontVideo
from back.db.model import (
    SettingFrontVideo,
    SettingFrontVideoInterpretation,
    SettingFrontVideoUpdate,
    TagToken,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(prefix="/video")


@router.get(
    "/category-startswith",
    response_model=List[TagToken],
    dependencies=[
        api_security([ScopeEnum.setting_front_video_category_startswith_get.value])
    ],
)
async def startswith_category(
    s: str = "", pagination: Pagination = Depends(get_pagination)
) -> List[TagToken]:
    return await CrudSettingFrontVideo.startswith_category(
        s, skip=pagination.skip, limit=pagination.size
    )


@router.get(
    "/tag-field-startswith",
    response_model=List[TagToken],
    dependencies=[
        api_security([ScopeEnum.setting_front_video_tag_field_startswith_get.value])
    ],
)
async def startswith_tag_field(
    s: str = "", pagination: Pagination = Depends(get_pagination)
) -> List[TagToken]:
    return await CrudSettingFrontVideo.startswith_tag_field(
        s, skip=pagination.skip, limit=pagination.size
    )


@router.get(
    "/interpretation",
    response_model=SettingFrontVideoInterpretation,
    dependencies=[
        api_security([ScopeEnum.setting_front_video_interpretation_get.value])
    ],
)
async def get_interpretation() -> SettingFrontVideoInterpretation:
    return await CrudSettingFrontVideo.get_interpretation()


@router.get(
    "/reset",
    response_model=SettingFrontVideo,
    dependencies=[api_security([ScopeEnum.setting_front_video_reset_get.value])],
)
async def reset() -> SettingFrontVideo:
    return await CrudSettingFrontVideo.reset()


@router.put("", dependencies=[api_security([ScopeEnum.setting_front_video_put.value])])
async def put(setting: SettingFrontVideoUpdate):
    return await CrudSettingFrontVideo.update(setting)
