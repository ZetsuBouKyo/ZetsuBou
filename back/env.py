from typing import Optional

from pydantic_settings import BaseSettings


class Env(BaseSettings):
    minio_volume: Optional[str] = None
    minio_root_password: Optional[str] = None
