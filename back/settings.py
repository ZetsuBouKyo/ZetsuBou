from enum import Enum
from pathlib import Path

from pydantic import BaseSettings
from pydantic.networks import EmailStr

from back.model.base import SourceProtocolEnum

default_setting_path = Path("etc", "settings.env")
elastic_index_prefix = "zetsubou"

if not default_setting_path.exists():
    default_setting_path = None


class DatabaseType(str, Enum):
    SQLITE: str = "sqlite"
    POSTGRESQL: str = "postgresql"


class AppMode(str, Enum):
    STANDALONE: str = "STANDALONE"
    CLUSTER: str = "CLUSTER"


class Setting(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 3000
    app_mode: AppMode = AppMode.STANDALONE
    app_timezone: str = "UTC"

    app_title: str = "ZetsuBou"
    app_front: str = "./front/dist"
    app_favicon: str = "/favicon.ico"
    app_statics: str = "./statics"

    app_docs_swagger_js_url: str = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"
    )
    app_docs_swagger_css_url: str = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css"
    )
    app_docs_redoc_js_url: str = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )

    app_user_gallery_preview_size: int = 40
    app_user_video_preview_size: int = 40
    app_user_img_preview_size: int = 40
    app_user_auto_play_time_interval: int = 5

    @property
    def app_user_front_setting(cls):
        prefix = "app_user_"
        # TODO: python 3.9 removeprefix
        return {
            key.replace(prefix, "", 1): cls.dict()[key]
            for key in cls.dict().keys()
            if key.startswith(prefix)
        }

    app_admin_name: str = "zetsubou"
    app_admin_email: EmailStr = (
        "zetsubou@example.com"  # TODO: be careful. This is not safe.
    )
    app_admin_password: str = "zetsubou"

    app_security_algorithm: str = "HS256"
    app_security_expired: int = 200  # minutes
    app_security_secret: str = "VadwSj8umrbeG8ro"

    app_logging_level: str = "WARNING"
    app_logging_formatter_fmt: str = "%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)-8s - %(message)s"  # noqa

    standalone_host: str = "0.0.0.0"
    standalone_port: int = 3001
    standalone_secure: bool = False

    @property
    def standalone_url(cls):
        if cls.standalone_secure:
            return f"https://{cls.standalone_host}:{cls.standalone_port}"
        return f"http://{cls.standalone_host}:{cls.standalone_port}"

    gallery_dir_fname: str = ".tag"
    gallery_backup_count: int = 3
    gallery_tag_fname: str = "gallery.json"
    gallery_imgs_fname: str = "imgs.json"

    database_type: DatabaseType = DatabaseType.POSTGRESQL
    database_url: str = "postgresql+asyncpg://zetsubou:zetsubou@localhost:5430/zetsubou"
    database_echo: bool = False

    elastic_urls: str = "http://localhost:9200"
    elastic_size: int = 40
    elastic_index_gallery: str = f"{elastic_index_prefix}-gallery"
    elastic_index_video: str = f"{elastic_index_prefix}-video"
    elastic_index_tag: str = f"{elastic_index_prefix}-tag"

    @property
    def elastic_hosts(cls):
        if not cls.elastic_urls:
            return []
        return cls.elastic_urls.split(",")

    storage_protocol: SourceProtocolEnum = SourceProtocolEnum.MINIO.value
    storage_expires_in_minutes: int = 7 * 24 * 60
    storage_cache: str = "zetsubou"
    storage_backup: str = "backup"

    storage_s3_aws_access_key_id: str = "admin"
    storage_s3_aws_secret_access_key: str = "wJalrXUtnFEMI"
    storage_s3_endpoint_url: str = "http://localhost:9000"

    minio_user: str = "admin"
    minio_password: str = "wJalrXUtnFEMI"
    minio_endpoint: str = "localhost:9000"
    minio_is_secure: str = "false"
    minio_expires_in_minutes: int = 7 * 24 * 60
    minio_cache_bucket_name: str = "zetsubou"
    minio_backup_bucket_name: str = "backup"

    @property
    def minio_secure(cls):
        if cls.minio_is_secure.lower() == "false":
            return False
        elif cls.minio_is_secure.lower() == "true":
            return True
        return False

    airflow_host: str = "http://localhost:8080"
    airflow_username: str = "airflow"
    airflow_password: str = "airflow"

    class Config:
        env_prefix = "zetsubou_"


setting = Setting(_env_file=str(default_setting_path))
