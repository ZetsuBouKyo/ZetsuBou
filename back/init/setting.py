from enum import Enum
from pathlib import Path

import typer
from back.settings import (
    DEFAULT_AIRFLOW_SETTING_NAME,
    DEFAULT_SETTING_HOME,
    DEFAULT_SETTING_NAME,
    ENV_PREFIX,
    Setting,
)

_help = """
Initialize the ZetsuBou webapp.
"""
app = typer.Typer(name="init", help=_help)


DEFAULT_SETTING = Setting()


class ModeEnum(str, Enum):
    HOST: str = "host"


def get_envs(setting: Setting) -> str:
    _setting = setting.dict()

    envs = []
    for key, value in _setting.items():
        if value is None:
            continue
        envs.append(f"{ENV_PREFIX}{key}={value}")

    envs.sort()
    return "\n".join(envs)


def write(file_path: Path, data: str):
    with file_path.open(mode="w") as fp:
        fp.write(data)


def init_settings(setting: Setting):
    setting_home = Path(DEFAULT_SETTING_HOME)
    setting_path = setting_home / DEFAULT_SETTING_NAME
    airflow_setting_path = setting_home / DEFAULT_AIRFLOW_SETTING_NAME

    envs = get_envs(setting)
    write(setting_path, envs)
    write(airflow_setting_path, envs)
