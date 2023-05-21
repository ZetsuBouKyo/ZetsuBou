import typer
from back.init.async_elasticsearch import create_gallery, create_video, init_indices
from back.model.elasticsearch import AnalyzerEnum
from back.session.async_elasticsearch import async_elasticsearch
from rich import print_json

from command.utils import sync
from elasticsearch.helpers import async_reindex

_help = """
Manipulate the Elasticsearch.
"""
app = typer.Typer(name="elasticsearch", help=_help)


@app.command()
@sync
async def create_gallery_index(index: str = typer.Argument(..., help="Index name.")):
    await create_gallery(async_elasticsearch, index)


@app.command()
@sync
async def create_video_index(index: str = typer.Argument(..., help="Index name.")):
    await create_video(async_elasticsearch, index)


@app.command()
@sync
async def delete(index: str = typer.Argument(..., help="Index name.")):
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
async def reindex(
    source_index: str = typer.Argument(..., help="Index name."),
    target_index: str = typer.Argument(..., help="Index name."),
):
    if not await async_elasticsearch.indices.exists(index=source_index):
        print(f"{source_index} not found")
        return
    if not await async_elasticsearch.indices.exists(index=target_index):
        print(f"{target_index} not found")
        return

    query = {"query": {"match_all": {}}}

    await async_reindex(
        async_elasticsearch,
        source_index=source_index,
        target_index=target_index,
        query=query,
    )


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


@app.command()
@sync
async def match_all(index: str = typer.Argument(..., help="Index name.")):
    query = {"match_all": {}}
    _resp = await async_elasticsearch.search(
        index=index, query=query, track_total_hits=True
    )
    print_json(data=_resp)
