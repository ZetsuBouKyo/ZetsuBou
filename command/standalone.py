import typer
from rich import print_json

from back.crud.standalone import get_storage_stat, sync_new_galleries
from back.model.base import SourceProtocolEnum
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


@app.command(name="get-storage-stat")
@sync
async def _get_storage_stat(
    protocol: SourceProtocolEnum = typer.Argument(..., help="Storage protocol."),
    storage_id: int = typer.Argument(..., help="Storage ID."),
):
    stat = await get_storage_stat(protocol, storage_id)
    print_json(data=stat.dict())
