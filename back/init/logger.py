from logging import Formatter
from logging.handlers import RotatingFileHandler

from back.logging import logger_webapp
from back.logging.utils import get_all_loggers
from back.settings import LoggingLevelEnum, setting

APP_LOGGING_LEVEL = setting.app_logging_level.value
APP_LOGGING_Path = "./logs/app.log"
APP_LOGGING_FORMATTER_FMT = setting.app_logging_formatter_fmt
IGNORE_LOGGERS = ["sqlalchemy", "botocore", "httpcore"]

handler = RotatingFileHandler(APP_LOGGING_Path, maxBytes=2 * 1024 * 1024, backupCount=3)
formatter = Formatter(fmt=APP_LOGGING_FORMATTER_FMT)
handler.setFormatter(formatter)


def init_loggers(logging_level: LoggingLevelEnum = APP_LOGGING_LEVEL):
    if type(logging_level) is not str:
        logging_level = logging_level.value
    loggers = get_all_loggers()
    for logger in loggers:
        skip = False
        for ignore_logger in IGNORE_LOGGERS:
            if logger.name.startswith(ignore_logger):
                skip = True
                continue
        if skip:
            continue
        logger.setLevel(logging_level)
        logger.addHandler(handler)


def init_zetsubou_logger(logging_level: LoggingLevelEnum = APP_LOGGING_LEVEL):
    if type(logging_level) is not str:
        logging_level = logging_level.value
    logger_webapp.setLevel(logging_level)
    logger_webapp.addHandler(handler)
