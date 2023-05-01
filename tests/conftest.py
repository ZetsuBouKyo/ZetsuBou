import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path.cwd()))

from app import app  # noqa: 402


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
