from back.settings import setting
from fastapi import APIRouter
from fastapi.responses import FileResponse

FRONT = setting.app_front

router = APIRouter()


@router.get("/favicon.ico")
async def favicon():
    return FileResponse(f"{FRONT}/favicon.ico", media_type="image/png")


@router.get("/robots.txt")
async def robots():
    return FileResponse(f"{FRONT}/robots.txt", media_type="image/png")
