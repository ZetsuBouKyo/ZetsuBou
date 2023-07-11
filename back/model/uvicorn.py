from enum import Enum

from uvicorn.config import LOG_LEVELS

UvicornLogLevelEnum = Enum("UvicornLogLevelEnum", {k: k for k, _ in LOG_LEVELS.items()})
