from typing import Union

from httpx import Response
from rich.console import Console
from rich.rule import Rule
from rich.style import Style
from rich.text import Text

from tests.general.logger import logger


def print_divider(
    title: Union[str, Text] = "",
    characters: str = "─",
    text_style: Union[str, Style] = "",
    rule_style: Union[str, Style] = "rule.line",
):
    if type(title) is str:
        title = Text(text=title, style=text_style)

    console = Console()
    console.print(
        Rule(
            title=title,
            characters=characters,
            style=rule_style,
        )
    )


def print_api_request(url: str, method: str, data: dict = None, params: dict = None):
    method = method.upper()
    logger.info(f"Request URL: {url}")
    logger.info(f"Request method: {method}")
    if data is not None:
        logger.info(f"Request data: {data}")
    if params is not None:
        logger.info(f"Request params: {params}")


def print_api_response(response: Response):
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text: {response.text}")
