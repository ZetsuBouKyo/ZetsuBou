from inspect import iscoroutinefunction
from logging import Logger
from typing import Any, Sequence, Union

from tests.general.logger import logger


async def cli_runner(
    f, args: Union[str, Sequence[str]] = [], logger: Logger = logger
) -> Any:
    args_str = " ".join(args)
    logger.info(f"args: {args_str}")

    unwrapped_f = f.__wrapped__
    if iscoroutinefunction(unwrapped_f):
        result = await unwrapped_f(*args)
    else:
        result = unwrapped_f(*args)
    logger.info(f"return: {result}")
    return result
