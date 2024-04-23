from typing import List

import typer
from elasticsearch.helpers import async_reindex
from rich import print_json

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.init.async_elasticsearch import (
    create_gallery,
    create_tag,
    create_video,
    init_indices,
)
from back.model.elasticsearch import AnalyzerEnum
from back.session.async_elasticsearch import get_async_elasticsearch
from lib.typer import ZetsuBouTyper

_help = """
Manipulate the Elasticsearch.
"""
app = ZetsuBouTyper(name="elasticsearch", help=_help)


@app.command()
async def create_gallery_index(index: str = typer.Argument(..., help="Index name.")):
    """
    Create gallery index.
    """
    async_elasticsearch = get_async_elasticsearch()
    await create_gallery(async_elasticsearch, index)
    await async_elasticsearch.close()


@app.command()
async def create_video_index(index: str = typer.Argument(..., help="Index name.")):
    """
    Create video index.
    """
    async_elasticsearch = get_async_elasticsearch()
    await create_video(async_elasticsearch, index)
    await async_elasticsearch.close()


@app.command()
async def create_tag_index(index: str = typer.Argument(..., help="Index name.")):
    """
    Create tag index.
    """
    async_elasticsearch = get_async_elasticsearch()
    await create_tag(get_async_elasticsearch(), index)
    await async_elasticsearch.close()


@app.command()
async def delete(index: str = typer.Argument(..., help="Index name.")):
    """
    Delete the index.
    """
    async_elasticsearch = get_async_elasticsearch()

    if index is None:
        return
    if not await async_elasticsearch.ping():
        return
    if await async_elasticsearch.indices.exists(index=index):
        await async_elasticsearch.indices.delete(index=index, ignore=[400, 404])

    await async_elasticsearch.close()


@app.command()
async def list_indices():
    """
    List the indices.
    """
    async_elasticsearch = get_async_elasticsearch()

    indices = await async_elasticsearch.indices.get_alias()
    for index in indices.keys():
        print(index)

    await async_elasticsearch.close()


@app.command()
async def init():
    """
    Initialize the indices if the index does not exist.
    """
    async_elasticsearch = get_async_elasticsearch()
    await init_indices(sesion=async_elasticsearch)
    await async_elasticsearch.close()


@app.command()
async def reset():
    """
    Delete the indices and Initialize the indices.
    """
    async_elasticsearch = get_async_elasticsearch()

    indices = await async_elasticsearch.indices.get_alias()
    for index in indices.keys():
        if await async_elasticsearch.indices.exists(index=index):
            await async_elasticsearch.indices.delete(index=index, ignore=[400, 404])
    await init_indices(sesion=async_elasticsearch)
    await async_elasticsearch.close()


@app.command()
async def reindex(
    source_index: str = typer.Argument(..., help="Index name."),
    target_index: str = typer.Argument(..., help="Index name."),
):
    """
    Reindex the indices.
    """
    async_elasticsearch = get_async_elasticsearch()

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

    await async_elasticsearch.close()


@app.command()
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
    async_elasticsearch = get_async_elasticsearch()

    print(f"index: {index}")
    print(f"analyzer: {analyzer}")
    print(f"text: {text}")
    body = {"text": text, "analyzer": analyzer}
    resp = await async_elasticsearch.indices.analyze(body=body, index=index)
    print_json(data=resp)

    await async_elasticsearch.close()


@app.command()
async def match_all(
    index: str = typer.Argument(..., help="Index name."),
    size: int = typer.Option(default=10, help="Size."),
):
    """
    Send `match_all` query.
    """
    async_elasticsearch = get_async_elasticsearch()

    query = {"match_all": {}}
    _resp = await async_elasticsearch.search(
        index=index, query=query, track_total_hits=True, size=size
    )
    print_json(data=_resp)

    await async_elasticsearch.close()


@app.command()
async def match_phrase_prefix(
    index: str = typer.Argument(..., help="Index name."),
    field: List[str] = typer.Option(default=..., help="Field name."),
    text: List[str] = typer.Option(default=..., help="Keywords."),
    size: int = typer.Option(default=10, help="Size."),
):
    """
    Send `match_phrase_prefix` query.
    """
    async_elasticsearch = get_async_elasticsearch()

    if len(field) != len(text):
        print("The number of fields and text do not correspond to each other.")
        return

    query = {
        "bool": {
            "should": [
                {"match_phrase_prefix": {field[i]: {"query": text[i]}}}
                for i in range(len(field))
            ]
        }
    }

    _resp = await async_elasticsearch.search(index=index, query=query, size=size)
    print_json(data=_resp)

    await async_elasticsearch.close()


@app.command()
async def get_field_names(index: str = typer.Argument(..., help="Index name.")):
    """
    Get the field names of the index.
    """
    async with CrudAsyncElasticsearchBase(index=index) as crud:
        _resp = await crud.get_field_names()
        print(_resp)


@app.command()
async def total(index: str = typer.Argument(..., help="Index name.")):
    """
    Get the total number of documents in specific index.
    """
    async_elasticsearch = get_async_elasticsearch()

    query = {"match_all": {}}
    _resp = await async_elasticsearch.search(
        index=index, query=query, track_total_hits=True
    )
    total = _resp.get("hits", {}).get("total", {}).get("value", None)
    print(f"total: {total}")

    await async_elasticsearch.close()


@app.command()
async def mapping(index: str = typer.Argument(..., help="Index name.")):
    """
    Get the mapping of the index.
    """
    async_elasticsearch = get_async_elasticsearch()

    _resp = await async_elasticsearch.indices.get_mapping(index=index)
    print_json(data=_resp)

    await async_elasticsearch.close()
