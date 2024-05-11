import logging
import sys
from pathlib import Path

import pytest
from _pytest.config import Config
from _pytest.reports import TestReport
from rich.console import Console

from back.init.logger import stream_handler
from back.logging import logger_zetsubou as back_logger
from back.logging.utils import get_all_loggers
from lib.httpx import ZetsuBouAsyncClient
from tests.general.logging import logger as cli_logger
from tests.general.summary import print_divider

sys.path.append(str(Path.cwd()))

from app import app  # noqa: 402


@pytest.fixture(scope="function")
def client() -> ZetsuBouAsyncClient:
    return ZetsuBouAsyncClient(app=app, base_url="http://test")


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker("info")


def pytest_sessionstart():
    loggers = get_all_loggers()
    for logger in loggers:
        logger.setLevel(logging.WARNING)
        logger.handlers = []
    back_logger.addHandler(stream_handler)
    back_logger.setLevel(logging.DEBUG)
    cli_logger.addHandler(stream_handler)
    cli_logger.setLevel(logging.DEBUG)


def pytest_report_teststatus(report: TestReport, config: Config):  # pragma: no cover
    if config.option.markexpr != "info":
        return

    console = Console()
    if report.when == "call":
        if report.failed:
            print_divider(title="failed", characters="=", text_style="red")
            return (report.outcome, "", "failed")
        elif report.passed:
            print_divider(title="passed", characters="=", text_style="green")
            return (report.outcome, "", "passed")
        elif report.skipped:
            print_divider(title="skipped", characters="=", text_style="white")
            return (report.outcome, "", "skipped")
    elif report.when == "setup":
        func_name = report.location[-1]
        console.print("\n")
        length = len(func_name) + 11
        top = "[green]╔" + "═" * length + "╗"
        console.print(top)
        console.print(f"[green]║ [blue]function [green]{func_name} [green]║")
        bottom = "[green]╚" + "═" * length + "╝"
        console.print(bottom)
