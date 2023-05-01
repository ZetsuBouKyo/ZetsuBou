from pydantic import BaseSettings


class Env(BaseSettings):
    minio_volume: str = None
    minio_root_password: str = None
