from pathlib import Path

import pytest

from lib.uvicorn.files import check_files, get_watched_files
from tests.general.logger import logger


@pytest.mark.asyncio(scope="session")
async def test_get_watched_files():
    cwd = Path.cwd()
    logger.info(f"Current path: {cwd}")
    files = get_watched_files()
    assert check_files(cwd, files)
