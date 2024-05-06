from fastapi import APIRouter

from back.settings import AppModeEnum, setting

from .airflow import router as _airflow
from .standalone import router as _standalone

APP_MODE = setting.app_mode

router = APIRouter(prefix="/task", tags=["Task"])
router.include_router(_airflow)

if APP_MODE == AppModeEnum.STANDALONE:
    router.include_router(_standalone)
