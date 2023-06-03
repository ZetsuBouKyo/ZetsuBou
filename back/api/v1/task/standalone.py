from back.crud.standalone import open_folder
from back.crud.standalone import sync_new_galleries as _sync_new_galleries
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.settings import setting
from fastapi import APIRouter

standalone_url = setting.standalone_url

router = APIRouter()


@router.get(
    "/gallery/g/{gallery_id}/open",
    dependencies=[api_security([ScopeEnum.task_standalone_gallery_open_get.name])],
)
async def get_open_gallery(gallery_id: str):
    await open_folder(gallery_id)


@router.get(
    "/sync-new-galleries",
    dependencies=[
        api_security([ScopeEnum.task_standalone_gallery_sync_new_galleries_get.name])
    ],
)
async def sync_new_galleries():
    await _sync_new_galleries()
