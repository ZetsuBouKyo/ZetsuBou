from logging import Logger
from pathlib import Path

import pytest

from lib.uvicorn.files import check_files, get_watched_files


@pytest.mark.asyncio(scope="session")
async def test_get_watched_files(logger: Logger):
    cwd = Path.cwd()
    logger.info(f"Current path: {cwd}")
    files = get_watched_files()
    assert check_files(cwd, files)
