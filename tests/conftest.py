import logging
import sys
from pathlib import Path

import pytest
from _pytest.reports import TestReport
from rich.console import Console

from back.init.logger import stream_handler
from back.logging.utils import get_all_loggers
from lib.httpx import ZetsuBouAsyncClient
from tests.general.logger import logger as _logger
from tests.general.summary import divider

sys.path.append(str(Path.cwd()))

from app import app  # noqa: 402


@pytest.fixture(scope="function")
def client() -> ZetsuBouAsyncClient:
    return ZetsuBouAsyncClient(app=app, base_url="http://test")


def pytest_sessionstart():
    loggers = get_all_loggers()
    for logger in loggers:
        logger.setLevel(logging.WARNING)
        logger.handlers = []
    _logger.addHandler(stream_handler)
    _logger.setLevel(logging.DEBUG)


def pytest_report_teststatus(report: TestReport):
    console = Console()
    if report.when == "call":
        if report.failed:
            divider(title="failed", characters="=", text_style="red")
            return (report.outcome, "", "failed")
        elif report.passed:
            divider(title="passed", characters="=", text_style="green")
            return (report.outcome, "", "passed")
        elif report.skipped:
            divider(title="skipped", characters="=", text_style="white")
            return (report.outcome, "", "skipped")
    elif report.when == "setup":
        func_name = report.location[-1]
        console.print("\n")
        console.print(f"[blue]function [green]{func_name}")
