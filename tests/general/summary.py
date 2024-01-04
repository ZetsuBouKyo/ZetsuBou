from typing import Union

from rich.console import Console
from rich.rule import Rule
from rich.style import Style
from rich.text import Text


def divider(
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
