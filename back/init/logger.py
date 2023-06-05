from logging import Formatter
from logging.handlers import RotatingFileHandler

from back.logging import logger_webapp
from back.logging.utils import get_all_loggers
from back.settings import setting

APP_LOGGING_LEVEL = setting.app_logging_level
APP_LOGGING_Path = "./logs/app.log"
APP_LOGGING_FORMATTER_FMT = setting.app_logging_formatter_fmt
IGNORE_LOGGERS = ["sqlalchemy", "botocore", "httpcore"]

handler = RotatingFileHandler(APP_LOGGING_Path, maxBytes=2 * 1024 * 1024, backupCount=3)
formatter = Formatter(fmt=APP_LOGGING_FORMATTER_FMT)
handler.setFormatter(formatter)


def init_loggers():
    loggers = get_all_loggers()
    for logger in loggers:
        skip = False
        for ignore_logger in IGNORE_LOGGERS:
            if logger.name.startswith(ignore_logger):
                skip = True
                continue
        if skip:
            continue
        logger.setLevel(APP_LOGGING_LEVEL)
        logger.addHandler(handler)


def init_zetsubou_logger():
    logger_webapp.setLevel(APP_LOGGING_LEVEL)
    logger_webapp.addHandler(handler)
