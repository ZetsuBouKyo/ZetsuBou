from pydantic import BaseModel


class SettingFrontGalleryCategory(BaseModel):
    id: int = None
    token_id: int
    enable: bool
