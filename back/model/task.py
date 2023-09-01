from enum import Enum
from typing import Optional

from pydantic import BaseModel

PREFIX = "zetsubou"


class ZetsuBouTaskProgressEnum(str, Enum):
    SYNC_STORAGE: str = f"{PREFIX}.task.progress.sync-storage"
    SYNC_STORAGES: str = f"{PREFIX}.task.progress.sync-storages"
    SYNC_NEW_GALLERIES: str = f"{PREFIX}.task.progress.sync-new-galleries"


class ZetsuBouTask(BaseModel):
    progress_id: Optional[str] = None
    progress: Optional[float] = None
