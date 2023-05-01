from back.crud.gallery import get_crud_gallery
from back.db.model import ScopeEnum
from back.dependency.security import api_security
from back.model.gallery import Gallery
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/{gallery_id}/tag",
    response_model=Gallery,
    dependencies=[api_security([ScopeEnum.gallery_tag_get.name])],
)
async def get_tag(gallery_id: str) -> Gallery:
    crud = await get_crud_gallery(gallery_id)
    return crud.gallery


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

    crud = await get_crud_gallery(gallery_id)
    return crud.update(gallery)
