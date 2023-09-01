from typing import Optional

from pydantic import BaseModel


class SettingFrontGalleryCategory(BaseModel):
    id: Optional[int] = None
    token_id: int
    enable: bool
