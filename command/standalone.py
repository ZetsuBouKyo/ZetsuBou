import typer

from back.crud.standalone import sync_new_galleries
from command.utils import sync

_help = """
Run the commands in standalone mode.

In standalone mode, all services must be run on the same machine and ZetsuBou webapp
must be run in terminal not in docker container.
"""

app = typer.Typer(name="standalone", help=_help)


@app.command(name="sync-new-galleries")
@sync
async def _sync_new_galleries():
    """
    Synchonize the galleries from the host path to the storage volume.
    """
    await sync_new_galleries()
