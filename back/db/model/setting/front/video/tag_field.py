from pydantic import BaseModel


class SettingFrontVideoTagField(BaseModel):
    id: int = None
    token_id: int
    enable: bool
