from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

from back.crud.async_video import CrudAsyncVideo
from back.dependency.security import view_security
from back.model.scope import ScopeEnum

from .query import router as query
from .tag import router as tag

router = APIRouter(prefix="/video", tags=["Video"])
router.include_router(query)
router.include_router(tag)


@router.get("/v/{video_id}", dependencies=[view_security([ScopeEnum.video_get.value])])
async def get_video(video_id: str) -> FileResponse:
    async with CrudAsyncVideo(video_id, is_from_setting_if_none=True) as crud:
        video_url = await crud.get_video()
    return RedirectResponse(url=video_url)


@router.get(
    "/v/{video_id}/cover",
    dependencies=[view_security([ScopeEnum.video_cover_get.value])],
)
async def get_cover(video_id: str) -> FileResponse:
    async with CrudAsyncVideo(video_id, is_from_setting_if_none=True) as crud:
        cover = await crud.get_cover()
    return RedirectResponse(url=cover)
