from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from back.settings import Setting, setting
from fastapi import APIRouter

router = APIRouter(prefix="/system")


@router.get(
    "",
    response_model=Setting,
    dependencies=[api_security([ScopeEnum.sys_setting_get.name])],
)
def get_system_settings() -> Setting:
    return setting
