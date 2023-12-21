from enum import Enum


class ZetsuBouEnvEnum(str, Enum):
    ZETSUBOU_ELASTIC_URLS: str = "ZETSUBOU_ELASTIC_URLS"
    ZETSUBOU_SETTING_PATH: str = "ZETSUBOU_SETTING_PATH"  # See `dags/cmd_tasks.py`
