import logging
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from back.init.logger import stream_handler
from tests.general.logger import logger as _logger

sys.path.append(str(Path.cwd()))

from app import app  # noqa: 402


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    _logger.addHandler(stream_handler)
    print("\n")
    return _logger
