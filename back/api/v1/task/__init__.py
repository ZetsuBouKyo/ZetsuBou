from back.db.model import ScopeEnum
from back.dependency.security import api_security
from back.settings import AppMode, setting
from fastapi import APIRouter

from .airflow import router as airflow
from .standalone import router as standalone

app_mode = setting.app_mode

router = APIRouter()

router.include_router(
    airflow,
    tags=["Task"],
    prefix="/cmd",
    dependencies=[api_security(ScopeEnum.task_cmd.name)],
)

if app_mode == AppMode.STANDALONE:
    router.include_router(standalone, prefix="/standalone")
