from back.crud.setting import (
    AIRFLOW_SETTING_PATH,
    update_airflow_settings,
    update_settings,
)
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.settings import Setting, setting
from fastapi import APIRouter

router = APIRouter(prefix="/system")


@router.get(
    "",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_get.name])],
)
def get_settings() -> Setting:
    return setting


@router.put(
    "",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_put.name])],
)
def put_settings(setting: Setting) -> Setting:
    update_settings(setting)
    return setting


@router.get(
    "/airflow",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_airflow_get.name])],
)
def get_airflow_settings() -> Setting:
    setting = Setting(_env_file=str(AIRFLOW_SETTING_PATH))
    return setting


@router.put(
    "/airflow",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_airflow_put.name])],
)
def put_airflow_settings(setting: Setting) -> Setting:
    update_airflow_settings(setting)
    return setting
