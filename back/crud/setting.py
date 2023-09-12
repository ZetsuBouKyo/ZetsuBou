from pathlib import Path

from back.settings import (
    DEFAULT_AIRFLOW_SETTING_NAME,
    DEFAULT_SETTING_HOME,
    DEFAULT_SETTING_NAME,
    ENV_PREFIX,
    Setting,
    setting,
)

DEFAULT_SETTING = Setting()
SETTING_HOME = Path(DEFAULT_SETTING_HOME)
SETTING_PATH = SETTING_HOME / DEFAULT_SETTING_NAME

AIRFLOW_SETTING_PATH = SETTING_HOME / DEFAULT_AIRFLOW_SETTING_NAME
if setting.airflow_simple_volume is not None:
    AIRFLOW_SIMPLE_PASSWORD_PATH = (
        Path(setting.airflow_simple_volume) / "standalone_admin_password.txt"
    )
else:
    AIRFLOW_SIMPLE_PASSWORD_PATH = None


def get_envs(setting: Setting) -> str:
    _setting = setting.model_dump()

    envs = []
    for key, value in _setting.items():
        if value is None:
            continue
        _key = ENV_PREFIX + key
        _key = _key.upper()
        envs.append(f"{_key}={value}")

    envs.sort()
    return "\n".join(envs)


def get_airflow_simple_password(
    password_path: Path = AIRFLOW_SIMPLE_PASSWORD_PATH,
) -> str:
    if password_path is None or not password_path.exists():
        raise FileNotFoundError(f"[Errno 2] No such file: '{password_path}'")

    with password_path.open(mode="r") as fp:
        password = fp.read()
    return password


def get_setting_example(field_name: str):
    schema = Setting.model_json_schema()
    properties = schema.get("properties", None)
    example = properties.get(field_name, {}).get("example", None)

    return example


def write_settings(file_path: Path, data: str, force: bool = False):
    if file_path.exists() and not force:
        return

    with file_path.open(mode="w") as fp:
        fp.write(data)


def is_setting(setting_path: Path = SETTING_PATH) -> bool:
    return setting_path.exists()


def is_airflow_setting(setting_path: Path = AIRFLOW_SETTING_PATH) -> bool:
    return setting_path.exists()


def update_settings(
    setting: Setting, setting_path: Path = SETTING_PATH, force: bool = False
):
    envs = get_envs(setting)
    write_settings(setting_path, envs, force=force)


def update_airflow_settings(
    setting: Setting, setting_path: Path = AIRFLOW_SETTING_PATH, force: bool = False
):
    envs = get_envs(setting)
    write_settings(setting_path, envs, force=force)
