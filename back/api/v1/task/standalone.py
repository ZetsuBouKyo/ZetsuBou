import httpx
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.settings import setting
from fastapi import APIRouter
from httpx import ConnectError

standalone_url = setting.standalone_url

router = APIRouter()


def _ping() -> bool:
    url = f"{standalone_url}/ping"
    try:
        resp = httpx.get(url)
    except ConnectError:
        return False

    if resp.status_code == 200:
        return True

    return False


@router.get(
    "/gallery/g/{gallery_id}/open",
    dependencies=[api_security([ScopeEnum.task_standalone_gallery_open_get.name])],
)
def get_open_gallery(gallery_id: str):
    url = f"{standalone_url}/open?gallery_id={gallery_id}"
    try:
        httpx.get(url)
    except ConnectError:
        return False
    return True


@router.get(
    "/gallery/sync-new-galleries",
    dependencies=[
        api_security([ScopeEnum.task_standalone_gallery_sync_new_galleries_get.name])
    ],
)
def sync_new_galleries():
    url = f"{standalone_url}/sync-new-galleries"
    try:
        httpx.get(url)
    except ConnectError:
        return False
    return True


@router.get(
    "/ping",
    dependencies=[api_security([ScopeEnum.task_standalone_ping_get.name])],
)
def ping():
    return _ping()
