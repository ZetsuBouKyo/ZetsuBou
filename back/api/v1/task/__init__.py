from back.settings import AppMode, setting
from fastapi import APIRouter

from .airflow import router as airflow
from .standalone import router as standalone

APP_MODE = setting.app_mode

router = APIRouter(prefix="/task", tags=["Task"])
router.include_router(airflow)

if APP_MODE == AppMode.STANDALONE:
    router.include_router(standalone)
