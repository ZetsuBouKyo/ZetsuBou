from logging import Logger
from pathlib import Path

import pytest
from uvicorn.config import Config
from uvicorn.server import Server

from lib.uvicorn.files import check_files


@pytest.mark.asyncio(scope="session")
async def test_change_reload(logger: Logger):
    from lib import uvicorn

    config = Config("test")
    server = Server(config=config)
    sock = config.bind_socket()
    ChangeReload = uvicorn.run.__globals__["ChangeReload"]
    watcher = ChangeReload(config, target=server.run, sockets=[sock])
    cwd = Path.cwd()
    logger.info(f"Current path: {cwd}")
    files = watcher.reload_paths
    watcher.should_restart()
    assert check_files(cwd, files)
