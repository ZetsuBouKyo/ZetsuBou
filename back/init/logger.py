import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

from rich.logging import RichHandler

from back.logging import logger_zetsubou
from back.logging.utils import get_all_loggers
from back.settings import LoggingLevelEnum, setting
from command.logging import logger_cli

APP_LOGGING_TO_FILE = setting.app_logging_to_file
APP_LOGGING_LIBS = setting.app_logging_libs
APP_LOGGING_LEVEL = setting.app_logging_level.value
APP_LOGGING_FORMATTER_FMT = setting.app_logging_formatter_fmt

APP_LOGGING_Path = "./logs/app.log"

IGNORE_LOGGERS = ["sqlalchemy", "botocore", "httpcore"]


STREAM_FMT = "%(name)s - %(message)s"

stream_formatter = Formatter(fmt=STREAM_FMT)
stream_handler = RichHandler()
stream_handler.setFormatter(stream_formatter)


UVICORN_LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "fmt": STREAM_FMT,
        },
        "access": {
            "()": "logging.Formatter",
            "fmt": STREAM_FMT,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "rich.logging.RichHandler",
        },
        "access": {
            "formatter": "access",
            "class": "rich.logging.RichHandler",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}


def init_zetsubou_logger(logging_level: LoggingLevelEnum = APP_LOGGING_LEVEL):
    if type(logging_level) is not str:
        logging_level = logging_level.value
    loggers = get_all_loggers()
    for logger in loggers:
        logger.setLevel(logging_level)
        logger.handlers = []

    logger_uvicorn_error = logging.getLogger("uvicorn.error")
    logger_uvicorn_access = logging.getLogger("uvicorn.access")

    if APP_LOGGING_TO_FILE:
        rotating_file_formatter = Formatter(fmt=APP_LOGGING_FORMATTER_FMT)
        rotating_file_handler = RotatingFileHandler(
            APP_LOGGING_Path, maxBytes=2 * 1024 * 1024, backupCount=3
        )
        rotating_file_handler.setFormatter(rotating_file_formatter)

        if not APP_LOGGING_LIBS:
            logger_zetsubou.addHandler(rotating_file_handler)
            logger_uvicorn_error.addHandler(rotating_file_handler)
            logger_uvicorn_access.addHandler(rotating_file_handler)
        else:
            for logger in loggers:
                logger.addHandler(rotating_file_handler)

    if not APP_LOGGING_LIBS:
        logger_zetsubou.addHandler(stream_handler)
        logger_cli.addHandler(stream_handler)
        logger_uvicorn_error.addHandler(stream_handler)
        logger_uvicorn_access.addHandler(stream_handler)
    else:
        for logger in loggers:
            logger.addHandler(stream_handler)
