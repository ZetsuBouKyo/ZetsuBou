from fastapi import APIRouter

from back.api.model.setting.front import FrontGeneralSetting
from back.crud.async_gallery import elasticsearch_gallery_analyzer
from back.crud.async_video import elasticsearch_video_analyzer
from back.dependency.security import api_security
from back.init.async_elasticsearch import (
    gallery_mappings,
    get_field_analyzer_from_mapping,
    video_mappings,
)
from back.model.scope import ScopeEnum
from back.settings import setting

from .gallery import router as gallery
from .video import router as video

APP_MODE = setting.app_mode

router = APIRouter(prefix="/front")
router.include_router(gallery)
router.include_router(video)


@router.get(
    "/general",
    response_model=FrontGeneralSetting,
    dependencies=[api_security([ScopeEnum.setting_front_general_get.name])],
)
async def get_general_setting() -> FrontGeneralSetting:
    _front_general_setting = {
        "app_mode": APP_MODE,
        "gallery": {
            "analyzer": {
                "field": get_field_analyzer_from_mapping(gallery_mappings),
                "keyword": elasticsearch_gallery_analyzer,
            }
        },
        "video": {
            "analyzer": {
                "field": get_field_analyzer_from_mapping(video_mappings),
                "keyword": elasticsearch_video_analyzer,
            }
        },
    }
    front_general_setting = FrontGeneralSetting(**_front_general_setting)
    return front_general_setting
