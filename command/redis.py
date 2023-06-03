import typer
from back.session.async_redis import async_redis

from command.utils import sync

app = typer.Typer(name="redis")


@app.command()
@sync
async def ping():
    await async_redis.ping()


@app.command()
@sync
async def list():
    async for key in async_redis.scan_iter("*"):
        print(key)


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
