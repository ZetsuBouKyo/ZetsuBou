from fastapi import APIRouter, Response, status

from back.crud.standalone import sync_new_galleries as _sync_new_galleries
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.model.task import ZetsuBouTask, ZetsuBouTaskProgressEnum
from back.session.async_redis import async_redis

router = APIRouter(prefix="/sync-new-galleries")


@router.get(
    "",
    dependencies=[
        api_security([ScopeEnum.task_standalone_gallery_sync_new_galleries_get.name])
    ],
)
async def sync_new_galleries(response: Response):
    progress = await async_redis.get(ZetsuBouTaskProgressEnum.SYNC_NEW_GALLERIES.value)
    if progress is not None:
        response.status_code = status.HTTP_201_CREATED
        return
    await _sync_new_galleries()


@router.get(
    "/progress",
    response_model=ZetsuBouTask,
    dependencies=[
        api_security([ScopeEnum.task_standalone_gallery_sync_new_galleries_get.name]),
    ],
)
async def get_progress():
    _progress = await async_redis.get(ZetsuBouTaskProgressEnum.SYNC_NEW_GALLERIES.value)
    if _progress is None:
        return ZetsuBouTask()

    return ZetsuBouTask(
        progress_id=ZetsuBouTaskProgressEnum.SYNC_NEW_GALLERIES.value,
        progress=float(_progress),
    )


@router.delete(
    "/progress",
    dependencies=[
        api_security([ScopeEnum.task_standalone_gallery_sync_new_galleries_get.name]),
    ],
)
async def delete_progress():
    await async_redis.delete(ZetsuBouTaskProgressEnum.SYNC_NEW_GALLERIES.value)
