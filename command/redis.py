from typing import List, Tuple

import typer

from back.session.async_redis import async_redis
from command.logging import logger
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
async def list(key: str = typer.Option(default="*", help="Redis key.")) -> List[str]:
    """
    List all keys.
    """
    keys = []
    async for key in async_redis.scan_iter(key):
        k = key.decode("utf-8")
        logger.info(k)
        keys.append(k)
    return keys


@app.command(name="list-pairs")
async def _list_pairs(
    key: str = typer.Option(default="*", help="Redis key.")
) -> List[Tuple[str, str]]:
    """
    List all key-value pairs.
    """
    pairs = []
    async for key, value in async_redis.list_pairs(key=key):
        k = key.decode("utf-8")
        v = value.decode("utf-8")
        logger.info(f"key: {k} value: {v}")
        pairs.append((k, v))
    return pairs


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
async def get(key: str = typer.Argument(..., help="Key.")) -> str:
    """
    Get the value of the key.
    """
    value = await async_redis.get(key)
    v = value.decode("utf-8")
    logger.info(f"key: {key}")
    logger.info(f"value: {v}")
    return v


@app.command()
async def flushall():
    """
    Delete all key-value pairs.
    """
    await async_redis.flushall()
