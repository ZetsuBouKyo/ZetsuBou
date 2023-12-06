from pydantic import BaseModel


class SettingFrontGalleryTagField(BaseModel):
    id: int
    token_id: int
    enable: bool
