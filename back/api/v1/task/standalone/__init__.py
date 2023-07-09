from fastapi import APIRouter

from back.crud.standalone import open_folder
from back.dependency.security import api_security
from back.model.scope import ScopeEnum

from .sync_new_galleries import router as sync_new_galleries

router = APIRouter(prefix="/standalone")
router.include_router(sync_new_galleries)


@router.get(
    "/gallery/g/{gallery_id}/open",
    dependencies=[api_security([ScopeEnum.task_standalone_gallery_open_get.name])],
)
async def get_open_gallery(gallery_id: str):
    await open_folder(gallery_id)
