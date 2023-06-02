import logging


def get_all_loggers():
    return [logging.getLogger(name) for name in logging.root.manager.loggerDict]


def set_level_for_all_loggers(level):
    loggers = get_all_loggers()
    for logger in loggers:
        logger.setLevel(level)
