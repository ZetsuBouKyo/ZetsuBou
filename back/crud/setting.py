from pathlib import Path

from back.settings import (
    DEFAULT_AIRFLOW_SETTING_NAME,
    DEFAULT_SETTING_HOME,
    DEFAULT_SETTING_NAME,
    ENV_PREFIX,
    Setting,
)

DEFAULT_SETTING = Setting()
SETTING_HOME = Path(DEFAULT_SETTING_HOME)
SETTING_PATH = SETTING_HOME / DEFAULT_SETTING_NAME
AIRFLOW_SETTING_PATH = SETTING_HOME / DEFAULT_AIRFLOW_SETTING_NAME


def get_envs(setting: Setting) -> str:
    _setting = setting.dict()

    envs = []
    for key, value in _setting.items():
        if value is None:
            continue
        envs.append(f"{ENV_PREFIX}{key}={value}")

    envs.sort()
    return "\n".join(envs)


def write_settings(file_path: Path, data: str):
    with file_path.open(mode="w") as fp:
        fp.write(data)


def update_settings(setting: Setting, setting_path: Path = SETTING_PATH):
    envs = get_envs(setting)
    write_settings(setting_path, envs)


def update_airflow_settings(
    setting: Setting, setting_path: Path = AIRFLOW_SETTING_PATH
):
    envs = get_envs(setting)
    write_settings(setting_path, envs)
