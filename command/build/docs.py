import json
from pathlib import Path
from textwrap import dedent, indent
from typing import List, Set

import typer

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from lib.typer import ZetsuBouTyper
from tests.back.utils.test_keyword import get_data

_help = """
Build the documentation.
"""
app = ZetsuBouTyper(name="docs", help=_help)


class CrudAsyncElasticsearchTest(CrudAsyncElasticsearchBase):
    @property
    def fields(self) -> List[str]:
        return ["tags.*"]

    async def get_field_names(self) -> Set[str]:
        return {"tags.language"}


async def get_search_grammar_example():
    docs_indent = "    "
    crud = CrudAsyncElasticsearchTest(is_from_setting_if_none=True)

    examples = "#### Examples\n"
    data = get_data()

    for d in data:
        example = "\n"
        if not d.show_docs:
            continue

        example += f"- {d.docs}\n\n"

        keyword_length = len(d.keywords) - 1
        example += '=== "Input"\n\n'
        first_keyword = ""
        for i, keyword in enumerate(d.keywords):
            keyword_block = ""

            keyword_block += f"""\
            ```sh
            {keyword}
            ```
            """
            keyword_block = dedent(keyword_block)

            if i == 0:
                first_keyword = keyword
            if i != keyword_length:
                keyword_block += "\nor\n\n"

            keyword_block = indent(keyword_block, docs_indent)
            example += keyword_block

        example += '\n=== "Elasticsearch"\n'
        elasticsearch_query = await crud.get_match_query(first_keyword)
        elasticsearch_query_str = json.dumps(
            elasticsearch_query, indent=4, ensure_ascii=False
        )
        elasticsearch_query_str = f"\n\n```json\n{elasticsearch_query_str}\n```\n"

        elasticsearch_query_str = indent(elasticsearch_query_str, docs_indent)

        example += elasticsearch_query_str

        example += "\n"

        examples += example
    return examples


@app.command()
async def print_search_grammar_examples(
    out: str = typer.Option(default="", help="Documentation path.")
):
    """
    Print examples of search grammar.
    """
    _out = Path(out)

    docs = ""

    examples = await get_search_grammar_example()
    docs += examples

    print(docs)
