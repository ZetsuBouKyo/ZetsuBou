from typing import List

from fastapi import APIRouter, Depends

from back.db.crud import CrudSettingFrontGallery
from back.db.model import (
    SettingFrontGallery,
    SettingFrontGalleryInterpretation,
    SettingFrontGalleryUpdate,
    TagToken,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(prefix="/gallery")


@router.get(
    "/category-startswith",
    response_model=List[TagToken],
    dependencies=[
        api_security([ScopeEnum.setting_front_gallery_category_startswith_get.name])
    ],
)
async def startwith_category(
    s: str = "", pagination: Pagination = Depends(get_pagination)
) -> List[TagToken]:
    return await CrudSettingFrontGallery.startwith_category(
        s, skip=pagination.skip, limit=pagination.size
    )


@router.get(
    "/tag-field-startswith",
    response_model=List[TagToken],
    dependencies=[
        api_security([ScopeEnum.setting_front_gallery_tag_field_startswith_get.name])
    ],
)
async def startwith_tag_field(
    s: str = "", pagination: Pagination = Depends(get_pagination)
) -> List[TagToken]:
    return await CrudSettingFrontGallery.startwith_tag_field(
        s, skip=pagination.skip, limit=pagination.size
    )


@router.get(
    "/interpretation",
    response_model=SettingFrontGalleryInterpretation,
    dependencies=[
        api_security([ScopeEnum.setting_front_gallery_interpretation_get.name])
    ],
)
async def get_interpretation() -> SettingFrontGalleryInterpretation:
    return await CrudSettingFrontGallery.get_interpretation()


@router.get(
    "/reset",
    response_model=SettingFrontGallery,
    dependencies=[api_security([ScopeEnum.setting_front_gallery_reset_get.name])],
)
async def reset() -> SettingFrontGallery:
    return await CrudSettingFrontGallery.reset()


@router.get(
    "",
    response_model=SettingFrontGallery,
    dependencies=[api_security([ScopeEnum.setting_front_gallery_get.name])],
)
async def get() -> SettingFrontGallery:
    return await CrudSettingFrontGallery.get()


@router.put("", dependencies=[api_security([ScopeEnum.setting_front_gallery_put.name])])
async def put(setting: SettingFrontGalleryUpdate):
    return await CrudSettingFrontGallery.update(setting)
