from typing import Optional

from pydantic import BaseModel


class SettingFrontVideoCategory(BaseModel):
    id: Optional[int] = None
    token_id: int
    enable: bool
