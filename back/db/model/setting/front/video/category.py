from pydantic import BaseModel


class SettingFrontVideoCategory(BaseModel):
    id: int = None
    token_id: int
    enable: bool
