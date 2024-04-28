import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from back.model.base import SourceProtocolEnum
from back.model.envs import ZetsuBouEnvEnum

_DEFAULT_SETTING_PATH = os.getenv(
    ZetsuBouEnvEnum.ZETSUBOU_SETTING_PATH.value, default=None
)

DEFAULT_SETTING_HOME = "./etc"
DEFAULT_SETTING_NAME = "settings.env"
DEFAULT_AIRFLOW_SETTING_NAME = "settings.airflow.env"

DEFAULT_ADMIN_EMAIL = "zetsubou@example.com"
DEFAULT_ADMIN_NAME = "zetsubou"
DEFAULT_ADMIN_PASSWORD = "zetsubou"

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


class LoggingLevelEnum(str, Enum):
    CRITICAL: str = "CRITICAL"
    FATAL: str = "FATAL"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"
    WARN: str = "WARN"
    INFO: str = "INFO"
    DEBUG: str = "DEBUG"
    NOTSET: str = "NOTSET"


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX)

    app_host: str = Field(
        default="0.0.0.0", title=f"{TITLE_PREFIX} Host", examples=["0.0.0.0"]
    )
    app_security: bool = True
    app_port: int = Field(
        default=3000,
        title=f"{TITLE_PREFIX} Port",
        description="Environment variable for service and docker-compose.",
        examples=["3000"],
    )
    app_mode: AppModeEnum = AppModeEnum.CLUSTER
    app_timezone: str = Field(default="UTC", title="Timezone", examples=["Asia/Taipei"])

    app_docs: bool = Field(
        default=True, title="Swagger", description="An API document."
    )
    app_redoc: bool = Field(default=True, title="ReDoc", description="An API document.")

    app_title: str = Field(default="ZetsuBou", title="APP title")
    app_front: str = "./front/dist"
    app_front_docs: str = "./front/doc_site"
    app_favicon: str = Field(
        default="/favicon.ico", title="Favicon", description="A favicon relative URL."
    )
    app_statics: str = "./statics"

    app_docs_swagger_js_url: str = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
        examples=["/statics/swagger-ui-bundle.js"],
    )
    app_docs_swagger_css_url: str = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
        examples=["/statics/swagger-ui.css"],
    )
    app_docs_redoc_js_url: str = Field(
        default="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        examples=["/statics/redoc.standalone.js"],
    )

    app_user_front_settings_gallery_image_auto_play_time_interval: int = 5
    app_user_front_settings_gallery_image_preview_size: int = 40
    app_user_front_settings_gallery_preview_size: int = 40
    app_user_front_settings_video_preview_size: int = 40

    def get_app_user_front_settings(self, user_id: int) -> dict:
        return {
            "user_id": user_id,
            "gallery_image_auto_play_time_interval": self.app_user_front_settings_gallery_image_auto_play_time_interval,
            "gallery_image_preview_size": self.app_user_front_settings_gallery_image_preview_size,
            "gallery_preview_size": self.app_user_front_settings_gallery_preview_size,
            "video_preview_size": self.app_user_front_settings_video_preview_size,
        }

    app_admin_name: str = DEFAULT_ADMIN_NAME
    app_admin_email: EmailStr = (
        DEFAULT_ADMIN_EMAIL  # TODO: be careful. This is not safe.
    )
    app_admin_password: str = DEFAULT_ADMIN_PASSWORD

    app_security_algorithm: str = "HS256"
    app_security_expired: int = 200  # minutes
    app_security_secret: str = Field(
        default="VadwSj8umrbeG8ro",
        description="Used to encrypt token. Must be changed.",
    )

    app_logging_libs: bool = Field(
        default=False,
        description="When this value is true, all loggers are attached to handlers.",
    )
    app_logging_to_file: bool = Field(
        default=False,
        description="If this value is true, the application will write the log.",
    )
    app_logging_level: LoggingLevelEnum = LoggingLevelEnum.WARNING.value
    app_logging_formatter_fmt: str = (
        "%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s"
    )

    app_gallery_sync_pages: bool = Field(
        default=False,
        description="If this value is true, the number of pictures in the folder will be counted during synchronisation. This value has a significant impact on performance.",
    )
    app_gallery_sync_pages_when_go_to_gallery: bool = Field(
        default=True,
        description="If this value is true, the number of gallery images will be updated when you go to the gallery page.",
    )

    standalone_storage_protocol: Optional[SourceProtocolEnum] = None
    standalone_storage_id: Optional[int] = None
    standalone_storage_minio_volume: Optional[str] = None
    standalone_sync_galleries_from_path: Optional[str] = None
    standalone_sync_galleries_to_path: Optional[str] = None

    gallery_dir_fname: str = ".tag"
    gallery_backup_count: int = 3
    gallery_tag_fname: str = "gallery.json"
    gallery_imgs_fname: str = "imgs.json"

    database_type: DatabaseTypeEnum = DatabaseTypeEnum.POSTGRESQL
    database_url: Optional[str] = Field(
        default=None,
        examples=["postgresql+asyncpg://zetsubou:zetsubou@localhost:5430/zetsubou"],
    )
    database_echo: bool = False
    database_port: Optional[int] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["5430"],
    )
    database_initialization: Optional[bool] = Field(
        default=True,
        description="If this value is true, the tables in database will be automatically generated and updated.",
    )

    elastic_urls: Optional[str] = Field(
        default=None, examples=["http://localhost:9200"]
    )
    elastic_size: int = 40
    elastic_index_gallery: str = f"{ELASTIC_INDEX_PREFIX}-gallery"
    elastic_index_video: str = f"{ELASTIC_INDEX_PREFIX}-video"
    elastic_index_tag: str = f"{ELASTIC_INDEX_PREFIX}-tag"
    elasticsearch_port: Optional[int] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["9200"],
    )

    @property
    def elastic_hosts(cls):
        if not cls.elastic_urls:
            return []
        return cls.elastic_urls.split(",")

    elasticsearch_delete_redundant_docs: Optional[bool] = Field(
        default=False,
        description="If the value is `True`, we will delete the documents that cannot be found in the storages during synchronization.",
        examples=[False],
    )

    storage_protocol: SourceProtocolEnum = SourceProtocolEnum.MINIO.value
    storage_expires_in_minutes: int = 7 * 24 * 60

    storage_cache: str = Field(
        default="zetsubou", description="ZetsuBou S3 storage bucket name."
    )
    storage_tests: str = Field(
        default="tests", description="ZetsuBou S3 storage prefix."
    )
    storage_tests_galleries: str = Field(
        default="galleries", description="ZetsuBou S3 storage prefix."
    )
    storage_tests_videos: str = Field(
        default="videos", description="ZetsuBou S3 storage prefix."
    )

    @property
    def storage_backup(cls):
        return f"{cls.storage_cache}/backup"

    storage_s3_aws_access_key_id: Optional[str] = Field(
        default=None, examples=["admin"]
    )
    storage_s3_aws_secret_access_key: Optional[str] = Field(
        default=None, examples=["wJalrXUtnFEMI"]
    )
    storage_s3_endpoint_url: Optional[str] = Field(
        default=None, examples=["http://localhost:9000"]
    )
    storage_s3_volume: Optional[str] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["./dev/volumes/minio"],
    )
    storage_s3_port: Optional[int] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["9000"],
    )
    storage_s3_console_port: Optional[int] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["9001"],
    )

    airflow_host: Optional[str] = Field(
        default=None, examples=["http://localhost:8080"]
    )
    airflow_username: Optional[str] = Field(default=None, examples=["airflow"])
    airflow_password: Optional[str] = Field(default=None, examples=["airflow"])
    airflow_create_admin: Optional[bool] = Field(
        default=True,
        description="If this value is true, an admin user will be created by `docker-compose.standalone.yml` at startup.",
    )
    airflow_web_server_port: Optional[int] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["8080"],
    )
    airflow_standalone_volume: Optional[str] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["./dev/volumes/airflow-standalone"],
    )
    airflow_download_volume: Optional[str] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["./dev/volumes/minio/download"],
    )

    redis_url: Optional[str] = Field(
        default=None, examples=["redis://localhost:6380/0"]
    )
    redis_port: Optional[int] = Field(
        default=None,
        description="Environment variable for docker-compose.",
        examples=["6380"],
    )

    test_volumes_database_sqlite: Optional[str] = Field(
        default="dev/volumes/tests/database/sqlite",
        description="Relative path to store the sqlite file.",
    )

    test_database_url_postgresql: Optional[str] = Field(
        default=None,
        examples=["postgresql+asyncpg://zetsubou:zetsubou@localhost:5430/zetsubou"],
    )

    @property
    def test_database_url_sqlite(cls):
        return f"sqlite+aiosqlite:///{cls.test_volumes_database_sqlite}/zetsubou.db"


setting = Setting(_env_file=str(DEFAULT_SETTING_PATH))
