import os
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings, Field
from pydantic.networks import EmailStr

from back.model.base import SourceProtocolEnum
from back.model.envs import ZetsuBouEnvEnum

_DEFAULT_SETTING_PATH = os.getenv(
    ZetsuBouEnvEnum.ZETSUBOU_SETTING_PATH.value, default=None
)

DEFAULT_SETTING_HOME = "./etc"
DEFAULT_SETTING_NAME = "settings.env"
DEFAULT_AIRFLOW_SETTING_NAME = "settings.airflow.env"

if _DEFAULT_SETTING_PATH is None:
    DEFAULT_SETTING_PATH = Path(DEFAULT_SETTING_HOME) / DEFAULT_SETTING_NAME
else:
    DEFAULT_SETTING_PATH = Path(_DEFAULT_SETTING_PATH)

ELASTIC_INDEX_PREFIX = "zetsubou"
ENV_PREFIX = "zetsubou_"
TITLE_PREFIX = "ZetsuBou"

if not DEFAULT_SETTING_PATH.exists():
    DEFAULT_SETTING_PATH = None


class DatabaseTypeEnum(str, Enum):
    SQLITE: str = "sqlite"
    POSTGRESQL: str = "postgresql"


class AppModeEnum(str, Enum):
    STANDALONE: str = "standalone"
    CLUSTER: str = "cluster"


class Setting(BaseSettings):
    app_host: str = Field(
        default="0.0.0.0", title=f"{TITLE_PREFIX} Host", exmaple="0.0.0.0"
    )
    app_security: bool = True
    app_port: int = Field(
        default=3000,
        title=f"{TITLE_PREFIX} Port",
        description="Environment variable for service and docker-compose.",
        example="3000",
    )
    app_mode: AppModeEnum = AppModeEnum.CLUSTER
    app_timezone: str = Field(default="UTC", title="Timezone", example="Asia/Taipei")

    app_docs: bool = True
    app_redoc: bool = True

    app_title: str = Field(default="ZetsuBou")
    app_front: str = "./front/dist"
    app_favicon: str = "/favicon.ico"
    app_statics: str = "./statics"

    app_docs_swagger_js_url: str = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
        example="/statics/swagger-ui-bundle.js",
    )
    app_docs_swagger_css_url: str = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
        example="/statics/swagger-ui.css",
    )
    app_docs_redoc_js_url: str = Field(
        default="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        example="/statics/redoc.standalone.js",
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
    app_security_secret: str = Field(
        default="VadwSj8umrbeG8ro",
        description="Used to encrypt token. Must be changed.",
    )

    app_logging_level: str = "WARNING"
    app_logging_formatter_fmt: str = "%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s"  # noqa

    standalone_storage_protocol: SourceProtocolEnum = None
    standalone_storage_id: int = None
    standalone_storage_minio_volume: str = None
    standalone_sync_galleries_from_path: str = None
    standalone_sync_galleries_to_path: str = None

    gallery_dir_fname: str = ".tag"
    gallery_backup_count: int = 3
    gallery_tag_fname: str = "gallery.json"
    gallery_imgs_fname: str = "imgs.json"

    database_type: DatabaseTypeEnum = DatabaseTypeEnum.POSTGRESQL
    database_url: str = Field(
        default=None,
        example="postgresql+asyncpg://zetsubou:zetsubou@localhost:5430/zetsubou",
    )
    database_echo: bool = False
    database_port: int = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="5430",
    )

    elastic_urls: str = Field(default=None, example="http://localhost:9200")
    elastic_size: int = 40
    elastic_index_gallery: str = f"{ELASTIC_INDEX_PREFIX}-gallery"
    elastic_index_video: str = f"{ELASTIC_INDEX_PREFIX}-video"
    elastic_index_tag: str = f"{ELASTIC_INDEX_PREFIX}-tag"
    elasticsearch_port: int = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="9200",
    )

    @property
    def elastic_hosts(cls):
        if not cls.elastic_urls:
            return []
        return cls.elastic_urls.split(",")

    storage_protocol: SourceProtocolEnum = SourceProtocolEnum.MINIO.value
    storage_expires_in_minutes: int = 7 * 24 * 60
    storage_cache: str = "zetsubou"
    storage_backup: str = "backup"

    storage_s3_aws_access_key_id: str = Field(default=None, example="admin")
    storage_s3_aws_secret_access_key: str = Field(default=None, example="wJalrXUtnFEMI")
    storage_s3_endpoint_url: str = Field(default=None, example="http://localhost:9000")
    storage_s3_volume: str = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="./dev/volumes/minio",
    )
    storage_s3_port: int = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="9000",
    )
    storage_s3_console_port: int = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="9001",
    )

    airflow_host: str = Field(default=None, example="http://localhost:8080")
    airflow_username: str = Field(default=None, example="airflow")
    airflow_password: str = Field(default=None, example="airflow")
    airflow_web_server_port: int = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="8080",
    )
    airflow_simple_volume: str = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="./dev/volumes/airflow-simple",
    )

    redis_url: str = Field(default=None, example="redis://localhost:6380/0")
    redis_port: int = Field(
        default=None,
        description="Environment variable for docker-compose.",
        example="6380",
    )

    class Config:
        env_prefix = ENV_PREFIX


setting = Setting(_env_file=str(DEFAULT_SETTING_PATH))
