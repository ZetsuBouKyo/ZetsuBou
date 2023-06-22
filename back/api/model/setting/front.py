from typing import Dict, List

from back.model.elasticsearch import AnalyzerEnum, ElasticsearchField
from back.settings import AppModeEnum
from pydantic import BaseModel


class FrontGeneralSettingAnalyzerBase(BaseModel):
    field: Dict[ElasticsearchField, List[AnalyzerEnum]] = {}
    keyword: Dict[AnalyzerEnum, List[ElasticsearchField]] = {}


class FrontGeneralSettingBase(BaseModel):
    analyzer: FrontGeneralSettingAnalyzerBase = FrontGeneralSettingAnalyzerBase()


class FrontGeneralSettingGallery(FrontGeneralSettingBase):
    ...


class FrontGeneralSettingVideo(FrontGeneralSettingBase):
    ...


class FrontGeneralSetting(BaseModel):
    app_mode: AppModeEnum = None
    gallery: FrontGeneralSettingGallery
    video: FrontGeneralSettingVideo

    class Config:
        use_enum_values = True
