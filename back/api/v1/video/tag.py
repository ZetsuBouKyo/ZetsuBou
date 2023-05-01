from back.crud.video import get_crud_video
from back.db.model import ScopeEnum
from back.dependency.security import api_security
from back.model.video import Video
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/v/{video_id}/tag",
    response_model=Video,
    dependencies=[api_security([ScopeEnum.video_tag_get.name])],
)
async def get_tag(video_id: str) -> Video:
    crud = await get_crud_video(video_id)
    return crud.video


@router.post(
    "/v/{video_id}/tag",
    response_model=Video,
    dependencies=[api_security([ScopeEnum.video_tag_post.name])],
)
async def post_tag(video_id: str, video: Video) -> Video:
    if video_id != video.id:
        raise HTTPException(
            status_code=409, detail="Conflict between post body and url parameter"
        )

    crud = await get_crud_video(video_id)
    return crud.update(video)
