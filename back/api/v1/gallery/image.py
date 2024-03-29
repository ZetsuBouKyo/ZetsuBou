from typing import List

from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

from back.crud.async_gallery import CrudAsyncGallery
from back.dependency.security import api_security, view_security
from back.model.scope import ScopeEnum

router = APIRouter(tags=["Gallery Image"])


@router.get(
    "/{gallery_id}/images",
    response_model=List[str],
    dependencies=[api_security([ScopeEnum.gallery_images_get.value])],
)
async def get_imgages(gallery_id: str) -> List[str]:
    async with CrudAsyncGallery(gallery_id, is_from_setting_if_none=True) as crud:
        filenames = await crud.get_image_filenames()
    return filenames


@router.get(
    "/{gallery_id}/cover",
    dependencies=[view_security([ScopeEnum.gallery_cover_get.value])],
)
async def get_cover(gallery_id: str) -> FileResponse:
    async with CrudAsyncGallery(gallery_id, is_from_setting_if_none=True) as crud:
        cover = await crud.get_cover()
    return RedirectResponse(url=cover)


@router.get(
    "/{gallery_id}/i/{img}",
    dependencies=[view_security([ScopeEnum.gallery_image_get.value])],
)
async def get_image(gallery_id: str, img: str) -> FileResponse:
    async with CrudAsyncGallery(gallery_id, is_from_setting_if_none=True) as crud:
        img_url = await crud.get_image(img)
    return RedirectResponse(url=img_url)
