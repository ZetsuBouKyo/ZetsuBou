import typer
from back.init.async_elasticsearch import init_indices
from back.model.elasticsearch import AnalyzerEnum
from back.session.async_elasticsearch import async_elasticsearch
from rich import print_json

from command.utils import sync

_help = """
Manipulate the Elasticsearch.
"""
app = typer.Typer(name="elasticsearch", help=_help)


@app.command()
@sync
async def delete(index: str = typer.Argument(default=None, help="Index name.")):
    """
    Delete the index.
    """

    if index is None:
        return
    if not await async_elasticsearch.ping():
        return
    if await async_elasticsearch.indices.exists(index=index):
        await async_elasticsearch.indices.delete(index=index, ignore=[400, 404])


@app.command()
@sync
async def list_indices():
    """
    List the indices.
    """

    indices = await async_elasticsearch.indices.get_alias()
    for index in indices.keys():
        print(index)


@app.command()
@sync
async def init():
    """
    Initialize the indices if the index does not exist.
    """

    await init_indices()


@app.command()
@sync
async def reset():
    """
    Delete the indices and Initialize the indices.
    """
    indices = await async_elasticsearch.indices.get_alias()
    for index in indices.keys():
        if await async_elasticsearch.indices.exists(index=index):
            await async_elasticsearch.indices.delete(index=index, ignore=[400, 404])
    await init_indices()


@app.command()
@sync
async def analyze(
    text: str = typer.Argument(..., help="Text for analyzing."),
    analyzer: AnalyzerEnum = typer.Option(
        default=AnalyzerEnum.DEFAULT.value, help="Analyzer name."
    ),
    index: str = typer.Option(default=None, help="Index name."),
):
    """
    Analyze the text string and return the resulting tokens.
    """
    print(f"index: {index}")
    print(f"analyzer: {analyzer}")
    print(f"text: {text}")
    body = {"text": text, "analyzer": analyzer}
    resp = await async_elasticsearch.indices.analyze(body=body, index=index)
    print_json(data=resp)
