import typer
from back.init.check import ping as _ping
from back.model.service import ServiceEnum
from command.utils import sync
from back.init.check import check_host_port

app = typer.Typer(name="service")


@app.command()
@sync
async def ping(service: ServiceEnum = typer.Option(default=None, help="Service name.")):
    """
    Ping the services.
    """
    print(await _ping(service=service))


@app.command()
def port(port: int = typer.Argument(..., help="Service port.")):
    """
    Return `False` if host port is available.
    """
    print(check_host_port(port))
