from typing import Dict, List

from back.model.elasticsearch import AnalyzerEnum, ElasticsearchField
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
    gallery: FrontGeneralSettingGallery
    video: FrontGeneralSettingVideo

    class Config:
        use_enum_values = True
