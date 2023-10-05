from fastapi import APIRouter, HTTPException

from back.crud.setting import (
    AIRFLOW_SETTING_PATH,
    is_airflow_setting,
    is_setting,
    update_airflow_settings,
    update_settings,
)
from back.dependency.security import api_security
from back.init.setting import init_settings_with_examples
from back.model.scope import ScopeEnum
from back.settings import (
    DEFAULT_AIRFLOW_SETTING_NAME,
    DEFAULT_SETTING_NAME,
    Setting,
    setting,
)

router = APIRouter(prefix="/system")


@router.get(
    "",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_get.value])],
)
def get_settings() -> Setting:
    return setting


@router.post(
    "",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_post.value])],
)
def post_settings(setting: Setting) -> Setting:
    if is_setting():
        HTTPException(
            status_code=409, detail=f"`{DEFAULT_SETTING_NAME}` already exists."
        )
    setting = init_settings_with_examples(setting)
    update_settings(setting)
    return setting


@router.put(
    "",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_put.value])],
)
def put_settings(setting: Setting) -> Setting:
    update_settings(setting, force=True)
    return setting


@router.get(
    "/airflow",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_airflow_get.value])],
)
def get_airflow_settings() -> Setting:
    setting = Setting(_env_file=str(AIRFLOW_SETTING_PATH))
    return setting


@router.post(
    "/airflow",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_airflow_post.value])],
)
def post_airflow_settings(setting: Setting) -> Setting:
    if is_airflow_setting():
        HTTPException(
            status_code=409, detail=f"`{DEFAULT_AIRFLOW_SETTING_NAME}` already exists."
        )
    setting = init_settings_with_examples(setting)
    update_airflow_settings(setting)
    return setting


@router.put(
    "/airflow",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.setting_system_airflow_put.value])],
)
def put_airflow_settings(setting: Setting) -> Setting:
    update_airflow_settings(setting)
    return setting
