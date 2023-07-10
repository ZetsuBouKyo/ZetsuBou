import asyncio
import sys
from functools import wraps
from inspect import iscoroutinefunction

from typer import Typer


class ZetsuBouTyper(Typer):
    def __init__(self, *args, loop_factory=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_factory = loop_factory

    def command(self, *args, **kwargs):
        decorator = super().command(*args, **kwargs)

        def add_runner(f):
            @wraps(f)
            def runner(*args, **kwargs):
                if sys.version_info >= (3, 11) and self.loop_factory:
                    with asyncio.Runner(loop_factory=self.loop_factory) as runner:
                        runner.run(f(*args, **kwargs))
                else:
                    asyncio.run(f(*args, **kwargs))

            if iscoroutinefunction(f):
                return decorator(runner)
            return decorator(f)

        return add_runner
