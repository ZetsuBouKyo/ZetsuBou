from back.schema.basic import Message
from back.settings import AppMode
from pydantic import BaseModel


class SyncMessage(Message):
    # TODO: HA
    is_sync: bool = False


class BasicSetting(BaseModel):
    app_mode: AppMode
