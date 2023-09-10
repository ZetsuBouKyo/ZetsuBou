from lib.typer import ZetsuBouTyper

from .print_search_grammar_examples import print_search_grammar_examples
from .print_web_search_analyzers import print_web_search_analyzers

_help = """
Build the documentation.
"""
app = ZetsuBouTyper(name="docs", help=_help)

app.command()(print_search_grammar_examples)
app.command()(print_web_search_analyzers)
