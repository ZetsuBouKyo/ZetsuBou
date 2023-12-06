from pydantic import BaseModel


class SettingFrontGalleryCategory(BaseModel):
    id: int
    token_id: int
    enable: bool
