import logging
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from back.init.logger import stream_handler
from back.logging.utils import get_all_loggers
from tests.general.logger import logger as _logger

sys.path.append(str(Path.cwd()))

from app import app  # noqa: 402


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    loggers = get_all_loggers()
    for logger in loggers:
        logger.setLevel(logging.WARNING)
        logger.handlers = []
    _logger.addHandler(stream_handler)
    _logger.setLevel(logging.DEBUG)
    print("\n")
    return _logger
