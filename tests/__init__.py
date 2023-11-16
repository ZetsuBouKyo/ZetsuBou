import logging

from back.logging.utils import get_all_loggers

loggers = get_all_loggers()
for logger in loggers:
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
