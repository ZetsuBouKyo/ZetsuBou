from enum import Enum

from pydantic import BaseModel

PREFIX = "zetsubou"


class ZetsuBouTaskProgressEnum(str, Enum):
    SYNC_STORAGE: str = f"{PREFIX}.task.progress.sync-storage"
    SYNC_STORAGES: str = f"{PREFIX}.task.progress.sync-storages"
    SYNC_NEW_GALLERIES: str = f"{PREFIX}.task.progress.sync-new-galleries"


class ZetsuBouTask(BaseModel):
    progress_id: str = None
    progress: float = None
