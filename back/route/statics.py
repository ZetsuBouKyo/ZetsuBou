from back.settings import setting
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

front = setting.app_front


@router.get("/favicon.ico")
async def favicon():
    return FileResponse(f"{front}/favicon.ico", media_type="image/png")


@router.get("/robots.txt")
async def robots():
    return FileResponse(f"{front}/robots.txt", media_type="image/png")
