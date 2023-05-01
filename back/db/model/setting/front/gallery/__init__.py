from typing import List

from pydantic import BaseModel

from ....tag.token import TagToken


class SettingFrontGalleryCreate(BaseModel):
    category_ids: List[int] = []
    tag_field_ids: List[int] = []


SettingFrontGallery = (
    SettingFrontGalleryUpdate
) = SettingFrontGalleryCreated = SettingFrontGalleryCreate


class SettingFrontGalleryInterpretation(BaseModel):
    categories: List[TagToken] = []
    tag_fields: List[TagToken] = []
