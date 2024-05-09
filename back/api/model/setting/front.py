from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from back.model.elasticsearch import ElasticsearchAnalyzerEnum, ElasticsearchField
from back.settings import AppModeEnum


class FrontGeneralSettingAnalyzerBase(BaseModel):
    field: Dict[ElasticsearchField, List[ElasticsearchAnalyzerEnum]] = {}
    keyword: Dict[ElasticsearchAnalyzerEnum, List[ElasticsearchField]] = {}


class FrontGeneralSettingBase(BaseModel):
    analyzer: FrontGeneralSettingAnalyzerBase = FrontGeneralSettingAnalyzerBase()


class FrontGeneralSettingGalleryGoto(BaseModel):
    sync_pages: Optional[bool] = None


class FrontGeneralSettingGallery(FrontGeneralSettingBase):
    goto: FrontGeneralSettingGalleryGoto


class FrontGeneralSettingVideo(FrontGeneralSettingBase): ...


class FrontGeneralSetting(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    app_mode: Optional[AppModeEnum] = None
    gallery: FrontGeneralSettingGallery
    video: FrontGeneralSettingVideo
