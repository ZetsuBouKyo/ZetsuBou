from fastapi import APIRouter

from back.crud.async_gallery import CrudAsyncGallery
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.schema.basic import Message

router = APIRouter(tags=["Gallery Operation"])


@router.delete(
    "/{gallery_id}/delete",
    response_model=Message,
    dependencies=[api_security([ScopeEnum.gallery_delete.value])],
)
async def delete(gallery_id: str) -> Message:
    async with CrudAsyncGallery(gallery_id, is_from_setting_if_none=True) as crud:
        detail = await crud.delete()
    return Message(detail=detail)
