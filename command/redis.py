import typer

from back.session.async_redis import async_redis, list_pairs
from command.utils import sync

app = typer.Typer(name="redis")


@app.command()
@sync
async def ping():
    await async_redis.ping()


@app.command()
@sync
async def list(key: str = typer.Option(default="*", help="Redis key.")):
    async for key in async_redis.scan_iter(key):
        print(key)


@app.command(name="list-pairs")
@sync
async def _list_pairs(key: str = typer.Option(default="*", help="Redis key.")):
    async for key, value in list_pairs(key=key):
        print(key, value)


@app.command()
@sync
async def set(
    key: str = typer.Argument(..., help="Key."),
    value: str = typer.Argument(..., help="Value."),
):
    await async_redis.set(key, value)


@app.command()
@sync
async def get(key: str = typer.Argument(..., help="Key.")):
    value = await async_redis.get(key)
    print(value)


@app.command()
@sync
async def flushall():
    await async_redis.flushall()
