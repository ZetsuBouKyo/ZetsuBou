import typer

from back.session.async_redis import async_redis, list_pairs
from lib.typer import ZetsuBouTyper

app = ZetsuBouTyper(name="redis")


@app.command()
async def ping():
    await async_redis.ping()


@app.command()
async def list(key: str = typer.Option(default="*", help="Redis key.")):
    async for key in async_redis.scan_iter(key):
        print(key)


@app.command(name="list-pairs")
async def _list_pairs(key: str = typer.Option(default="*", help="Redis key.")):
    async for key, value in list_pairs(key=key):
        print(key, value)


@app.command()
async def set(
    key: str = typer.Argument(..., help="Key."),
    value: str = typer.Argument(..., help="Value."),
):
    await async_redis.set(key, value)


@app.command()
async def get(key: str = typer.Argument(..., help="Key.")):
    value = await async_redis.get(key)
    print(value)


@app.command()
async def flushall():
    await async_redis.flushall()
