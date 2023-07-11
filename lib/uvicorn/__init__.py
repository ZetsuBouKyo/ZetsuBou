import logging
from pathlib import Path
from socket import socket
from typing import Callable, List, Optional

from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import FileFilter
from watchfiles import watch

from lib.uvicorn.files import get_watched_files

logger = logging.getLogger("uvicorn.error")


class WatchFilesReload(BaseReload):
    def __init__(
        self,
        config: Config,
        target: Callable[[Optional[List[socket]]], None],
        sockets: List[socket],
    ) -> None:
        super().__init__(config, target, sockets)
        self.reloader_name = "WatchFiles"
        self.reload_paths = get_watched_files()

        self.watch_filter = FileFilter(config)

        self.watcher = watch(
            *self.reload_paths,
            watch_filter=None,
            stop_event=self.should_exit,
            # using yield_on_timeout here mostly to make sure tests don't
            # hang forever, won't affect the class's behavior
            yield_on_timeout=True,
        )

    def should_restart(self) -> Optional[List[Path]]:
        self.pause()

        changes = next(self.watcher)
        if changes:
            unique_paths = {Path(c[1]) for c in changes}
            return [p for p in unique_paths]
        return None


ChangeReload = WatchFilesReload

import uvicorn

uvicorn.run.__globals__["ChangeReload"] = ChangeReload
run = uvicorn.run
