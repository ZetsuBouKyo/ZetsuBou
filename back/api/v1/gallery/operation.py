from back.crud.async_gallery import get_crud_async_gallery
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.schema.basic import Message
from back.settings import setting
from fastapi import APIRouter

router = APIRouter()
app_mode = setting.app_mode


@router.delete(
    "/{gallery_id}/delete",
    response_model=Message,
    dependencies=[api_security([ScopeEnum.gallery_delete.name])],
)
async def delete(gallery_id: str) -> Message:
    crud = await get_crud_async_gallery(gallery_id)
    detail = await crud.delete()
    return Message(detail=detail)
