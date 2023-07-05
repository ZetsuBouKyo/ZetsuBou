from fastapi import APIRouter

from back.settings import AppModeEnum, setting

from .airflow import router as airflow
from .standalone import router as standalone

APP_MODE = setting.app_mode

router = APIRouter(prefix="/task", tags=["Task"])
router.include_router(airflow)

if APP_MODE == AppModeEnum.STANDALONE:
    router.include_router(standalone)
