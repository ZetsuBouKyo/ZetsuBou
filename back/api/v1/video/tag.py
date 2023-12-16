from fastapi import APIRouter, HTTPException

from back.crud.async_video import CrudAsyncVideo, get_video_by_video_id
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.model.video import Video

router = APIRouter()


@router.get(
    "/v/{video_id}/tag",
    response_model=Video,
    dependencies=[api_security([ScopeEnum.video_tag_get.value])],
)
async def get_tag(video_id: str) -> Video:
    video = await get_video_by_video_id(video_id)
    return video


@router.post(
    "/v/{video_id}/tag",
    response_model=Video,
    dependencies=[api_security([ScopeEnum.video_tag_post.value])],
)
async def post_tag(video_id: str, video: Video) -> Video:
    if video_id != video.id:
        raise HTTPException(
            status_code=409, detail="Conflict between post body and url parameter"
        )
    async with CrudAsyncVideo(video_id, is_from_setting_if_none=True) as crud:
        res = await crud.update(video)
    return res
