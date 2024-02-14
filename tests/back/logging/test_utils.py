from logging import DEBUG

from back.logging.utils import get_all_loggers, set_level_for_all_loggers


def test_logging_utils():
    set_level_for_all_loggers(DEBUG)
    loggers = get_all_loggers()
    for logger in loggers:
        assert logger.level == DEBUG
