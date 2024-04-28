from typing import List

from pydantic import BaseModel

from back.db.model.tag.token import TagToken


class SettingFrontVideoCreate(BaseModel):
    category_ids: List[int] = []
    tag_field_ids: List[int] = []


SettingFrontVideo = SettingFrontVideoUpdate = SettingFrontVideoCreated = (
    SettingFrontVideoCreate
)


class SettingFrontVideoInterpretation(BaseModel):
    categories: List[TagToken] = []
    tag_fields: List[TagToken] = []
