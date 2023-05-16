from back.crud.gallery import get_crud_async_gallery
from back.db.model import ScopeEnum
from back.dependency.security import api_security
from back.schema.basic import Message
from back.session.standalone import standalone_client
from back.settings import AppMode, setting
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


@router.get(
    "/{gallery_id}/open", dependencies=[api_security([ScopeEnum.gallery_open_get.name])]
)
def open_folder(gallery_id: str):
    if app_mode != AppMode.STANDALONE:
        return False
    return standalone_client.open_folder(gallery_id)
