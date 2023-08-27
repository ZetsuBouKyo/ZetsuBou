from lib.typer import ZetsuBouTyper

from .print_search_grammar_examples import print_search_grammar_examples

_help = """
Build the documentation.
"""
app = ZetsuBouTyper(name="docs", help=_help)

app.command()(print_search_grammar_examples)
