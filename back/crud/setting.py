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
        _key = ENV_PREFIX + key
        _key = _key.upper()
        envs.append(f"{_key}={value}")

    envs.sort()
    return "\n".join(envs)


def init_settings(setting: Setting) -> Setting:
    new_setting = {}
    schema = Setting.schema()
    properties = schema.get("properties", None)

    for field_name, field_value in setting.dict().items():
        if field_value is None:
            example = properties.get(field_name, {}).get("example", None)
            if example is None:
                continue
            new_setting[field_name] = example
        else:
            new_setting[field_name] = field_value

    return Setting(**new_setting)


def write_settings(file_path: Path, data: str):
    with file_path.open(mode="w") as fp:
        fp.write(data)


def is_setting(setting_path: Path = SETTING_PATH) -> bool:
    return setting_path.exists()


def is_airflow_setting(setting_path: Path = AIRFLOW_SETTING_PATH) -> bool:
    return setting_path.exists()


def update_settings(setting: Setting, setting_path: Path = SETTING_PATH):
    envs = get_envs(setting)
    write_settings(setting_path, envs)


def update_airflow_settings(
    setting: Setting, setting_path: Path = AIRFLOW_SETTING_PATH
):
    envs = get_envs(setting)
    write_settings(setting_path, envs)
