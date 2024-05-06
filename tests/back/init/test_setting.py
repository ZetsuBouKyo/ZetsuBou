from back.init.setting import init_example_settings, init_settings_with_examples
from back.settings import Setting
from tests.general.logging import logger


def test_init_settings_with_examples():
    s = Setting()
    s = init_settings_with_examples(s)
    logger.info(f"\n{s.model_dump_json(indent=4)}")
    assert type(s) is Setting


def test_init_example_settings():
    s = init_example_settings()
    logger.info(s.model_dump_json(indent=4))
    assert type(s) is Setting
