from fastapi import APIRouter, HTTPException

from back.crud.async_gallery import get_crud_async_gallery, get_gallery_by_gallery_id
from back.dependency.security import api_security
from back.model.gallery import Gallery
from back.model.scope import ScopeEnum

router = APIRouter(tags=["Gallery Tag"])


@router.get(
    "/{gallery_id}/tag",
    response_model=Gallery,
    dependencies=[api_security([ScopeEnum.gallery_tag_get.name])],
)
async def get_tag(gallery_id: str) -> Gallery:
    gallery = await get_gallery_by_gallery_id(gallery_id)
    return gallery


@router.post(
    "/{gallery_id}/tag",
    response_model=Gallery,
    dependencies=[api_security([ScopeEnum.gallery_tag_post.name])],
)
async def post_tag(gallery_id: str, gallery: Gallery) -> Gallery:
    if gallery_id != gallery.id:
        raise HTTPException(
            status_code=409, detail="Conflict between post body and url parameter"
        )

    crud = await get_crud_async_gallery(gallery_id)
    return await crud.update(gallery)
