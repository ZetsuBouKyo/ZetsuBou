import typer

from back.session.async_redis import async_redis
from lib.typer import ZetsuBouTyper

_help = """
Manipulate the Redis.
"""
app = ZetsuBouTyper(name="redis", help=_help)


@app.command()
async def ping():
    """
    Ping the redis server.
    """
    await async_redis.ping()


@app.command()
async def list(key: str = typer.Option(default="*", help="Redis key.")):
    """
    List all keys.
    """
    async for key in async_redis.scan_iter(key):
        print(key)


@app.command(name="list-pairs")
async def _list_pairs(key: str = typer.Option(default="*", help="Redis key.")):
    """
    List all key-value pairs.
    """
    async for key, value in async_redis.list_pairs(key=key):
        print(key, value)


@app.command()
async def set(
    key: str = typer.Argument(..., help="Key."),
    value: str = typer.Argument(..., help="Value."),
):
    """
    Set a key-value pair.
    """
    await async_redis.set(key, value)


@app.command()
async def get(key: str = typer.Argument(..., help="Key.")):
    """
    Get the value of the key.
    """
    value = await async_redis.get(key)
    print(value)


@app.command()
async def flushall():
    """
    Delete all key-value pairs.
    """
    await async_redis.flushall()
