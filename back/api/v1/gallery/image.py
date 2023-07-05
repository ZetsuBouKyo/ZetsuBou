from typing import List

from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

from back.crud.async_gallery import get_crud_async_gallery
from back.dependency.security import api_security, view_security
from back.model.scope import ScopeEnum

router = APIRouter(tags=["Gallery Image"])


@router.get(
    "/{gallery_id}/images",
    response_model=List[str],
    dependencies=[api_security([ScopeEnum.gallery_images_get.name])],
)
async def get_imgages(gallery_id: str) -> List[str]:
    crud = await get_crud_async_gallery(gallery_id)
    return await crud.get_image_filenames()


@router.get(
    "/{gallery_id}/cover",
    dependencies=[view_security([ScopeEnum.gallery_cover_get.name])],
)
async def get_cover(gallery_id: str) -> FileResponse:
    crud = await get_crud_async_gallery(gallery_id)
    cover = await crud.get_cover()
    return RedirectResponse(url=cover)


@router.get(
    "/{gallery_id}/i/{img}",
    dependencies=[view_security([ScopeEnum.gallery_image_get.name])],
)
async def get_image(gallery_id: str, img: str) -> FileResponse:
    crud = await get_crud_async_gallery(gallery_id)
    img_url = await crud.get_image(img)
    return RedirectResponse(url=img_url)
