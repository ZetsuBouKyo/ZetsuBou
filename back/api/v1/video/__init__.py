from back.crud.async_video import get_crud_async_video
from back.dependency.security import view_security
from back.model.scope import ScopeEnum
from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

from .query import router as query
from .tag import router as tag

router = APIRouter(prefix="/video", tags=["Video"])
router.include_router(query)
router.include_router(tag)


@router.get("/v/{video_id}", dependencies=[view_security([ScopeEnum.video_get.name])])
async def get_video(video_id: str) -> FileResponse:
    crud = await get_crud_async_video(video_id)
    video_url = await crud.get_video()
    return RedirectResponse(url=video_url)


@router.get(
    "/v/{video_id}/cover",
    dependencies=[view_security([ScopeEnum.video_cover_get.name])],
)
async def get_cover(video_id: str) -> FileResponse:
    crud = await get_crud_async_video(video_id)
    cover = await crud.get_cover()
    return RedirectResponse(url=cover)
