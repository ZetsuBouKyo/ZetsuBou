from uuid import uuid4


def test_settings():
    import os

    from back.model.envs import ZetsuBouEnvEnum

    zetsubou_setting_path = f"./dev/volumes/tests/{str(uuid4())}"
    os.environ[ZetsuBouEnvEnum.ZETSUBOU_SETTING_PATH.value] = zetsubou_setting_path
    os.environ[ZetsuBouEnvEnum.ZETSUBOU_ELASTIC_URLS.value] = ""

    from importlib import reload

    from back import settings

    reload(settings)
    assert settings._DEFAULT_SETTING_PATH == zetsubou_setting_path
    assert settings.DEFAULT_SETTING_PATH is None

    assert len(settings.setting.elastic_hosts) == 0
