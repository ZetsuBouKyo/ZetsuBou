from pydantic import BaseModel


class SettingFrontGalleryTagField(BaseModel):
    id: int = None
    token_id: int
    enable: bool
