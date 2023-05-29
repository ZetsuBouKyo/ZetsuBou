from back.model.scope import ScopeEnum
from back.dependency.security import api_security
from back.settings import Setting, setting
from fastapi import APIRouter

from ..model.sys import BasicSetting

app_mode = setting.app_mode
router = APIRouter()


@router.get(
    "/setting",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.sys_setting_get.name])],
)
def get_setting() -> Setting:
    return setting


@router.get(
    "/basic-setting",
    response_model=BasicSetting,
    dependencies=[api_security([ScopeEnum.sys_basic_setting_get.name])],
)
def get_basic_setting():
    basic_setting = BasicSetting(app_mode=app_mode)
    return basic_setting
