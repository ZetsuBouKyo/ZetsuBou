import logging
from logging import Logger
from typing import List


def get_all_loggers() -> List[Logger]:
    return [logging.getLogger(name) for name in logging.root.manager.loggerDict]


def set_level_for_all_loggers(level):
    loggers = get_all_loggers()
    for logger in loggers:
        logger.setLevel(level)
