from back.init.check import check_host_port
from back.crud.setting import (
    get_setting_example,
    update_settings,
    update_airflow_settings,
    get_airflow_simple_password,
)
from back.settings import Setting
from typing import List


def get_port(port: int, max_tries: int = 10, excludes: List[int] = []) -> int:
    tries = 0
    while check_host_port(port) or port in excludes:
        port += 1
        tries += 1
        if tries >= max_tries:
            raise ValueError  # TODO:
    return port


def init_settings_with_examples(setting: Setting) -> Setting:
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


def init_example_settings(setting: Setting = None):
    # app
    if setting is None:
        setting = Setting()
    app_port = int(get_setting_example("app_port"))
    app_port = get_port(app_port)
    excludes = [app_port]
    setting.app_port = app_port

    # database
    database_port = int(get_setting_example("database_port"))
    database_port = get_port(database_port, excludes=excludes)
    excludes.append(database_port)

    setting.database_port = database_port
    setting.database_url = (
        f"postgresql+asyncpg://zetsubou:zetsubou@localhost:{database_port}/zetsubou"
    )

    # elasticsearch
    elasticsearch_port = int(get_setting_example("elasticsearch_port"))
    elasticsearch_port = get_port(elasticsearch_port, excludes=excludes)
    excludes.append(elasticsearch_port)

    setting.elasticsearch_port = elasticsearch_port
    setting.elastic_urls = f"http://localhost:{elasticsearch_port}"

    # storage
    storage_s3_port = int(get_setting_example("storage_s3_port"))
    storage_s3_port = get_port(storage_s3_port, excludes=excludes)
    excludes.append(storage_s3_port)
    storage_s3_console_port = int(get_setting_example("storage_s3_console_port"))
    storage_s3_console_port = get_port(storage_s3_console_port, excludes=excludes)
    excludes.append(storage_s3_console_port)

    setting.storage_s3_port = storage_s3_port
    setting.storage_s3_console_port = storage_s3_console_port
    setting.storage_s3_endpoint_url = f"http://localhost:{storage_s3_port}"

    # airflow
    airflow_web_server_port = int(get_setting_example("airflow_web_server_port"))
    airflow_web_server_port = get_port(airflow_web_server_port, excludes=excludes)
    excludes.append(airflow_web_server_port)

    setting.airflow_web_server_port = airflow_web_server_port
    setting.airflow_host = f"http://localhost:{airflow_web_server_port}"
    if setting.airflow_username is None:
        setting.airflow_username = "admin"
    if setting.airflow_password is None:
        setting.airflow_password = get_airflow_simple_password()

    # redis
    redis_port = int(get_setting_example("redis_port"))
    redis_port = get_port(redis_port, excludes=excludes)
    excludes.append(redis_port)

    setting.redis_port = redis_port
    setting.redis_url = f"redis://localhost:{redis_port}/0"

    setting = init_settings_with_examples(setting)
    update_settings(setting)
    update_airflow_settings(setting)
