from typing import Dict, List, Optional

from pydantic import BaseModel

from back.model.elasticsearch import AnalyzerEnum, ElasticsearchField
from back.settings import AppModeEnum


class FrontGeneralSettingAnalyzerBase(BaseModel):
    field: Dict[ElasticsearchField, List[AnalyzerEnum]] = {}
    keyword: Dict[AnalyzerEnum, List[ElasticsearchField]] = {}


class FrontGeneralSettingBase(BaseModel):
    analyzer: FrontGeneralSettingAnalyzerBase = FrontGeneralSettingAnalyzerBase()


class FrontGeneralSettingGalleryGoto(BaseModel):
    sync_pages: Optional[bool] = None


class FrontGeneralSettingGallery(FrontGeneralSettingBase):
    goto: FrontGeneralSettingGalleryGoto


class FrontGeneralSettingVideo(FrontGeneralSettingBase):
    ...


class FrontGeneralSetting(BaseModel):
    app_mode: Optional[AppModeEnum] = None
    gallery: FrontGeneralSettingGallery
    video: FrontGeneralSettingVideo

    class Config:
        use_enum_values = True
