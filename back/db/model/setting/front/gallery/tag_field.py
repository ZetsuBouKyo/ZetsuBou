from typing import Optional

from pydantic import BaseModel


class SettingFrontGalleryTagField(BaseModel):
    id: Optional[int] = None
    token_id: int
    enable: bool
