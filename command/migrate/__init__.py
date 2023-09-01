import time
from enum import Enum

import typer
from elasticsearch import AsyncElasticsearch

from back.crud.async_sync import get_crud_sync
from back.init.async_elasticsearch import create_gallery
from back.model.base import SourceProtocolEnum
from back.model.gallery import Gallery
from back.model.video import Video
from back.settings import setting
from lib.typer import ZetsuBouTyper

_help = """
Migrate the data to the new version.
"""
app = ZetsuBouTyper(name="migrate", help=_help)

ELASTICSEARCH_URLS = setting.elastic_urls


class StorageCategoryEnum(str, Enum):
    gallery: str = "gallery"
    video: str = "video"


def gallery_callback(source: Gallery) -> Gallery:
    src = [s for s in source.src if type(s) is str]
    source.src = src
    return source


def video_callback(source: Video) -> Video:
    src = [s for s in source.src if type(s) is str]
    source.src = src
    return source


@app.command(
    name="storage",
)
async def _storage(
    protocol: SourceProtocolEnum = typer.Argument(..., help="Storage protocol."),
    storage_id: int = typer.Argument(..., help="Storage ID."),
    category: StorageCategoryEnum = typer.Argument(..., help="Storage category."),
    progress: bool = typer.Option(
        default=True, help="Send progress information to Redis."
    ),
    elasticsearch_urls: str = typer.Option(
        default=ELASTICSEARCH_URLS, help="Elasticsearch URLs separated by `,`."
    ),
    target_index: str = typer.Option(default=None, help="Target Elasticsearch index."),
):
    """
    Synchronize the storage with protocol and storage ID.
    """

    # create `target_index` if it is not None and does not exist
    elasticsearch_hosts = elasticsearch_urls.split(",")
    async_elasticsearch = AsyncElasticsearch(hosts=elasticsearch_hosts)
    if target_index is not None:
        await create_gallery(async_elasticsearch, target_index)

    ti = time.time()

    if type(category) is not str:
        category = category.value

    if category == StorageCategoryEnum.gallery.value:
        crud = await get_crud_sync(
            protocol,
            storage_id,
            is_progress=progress,
            callback=gallery_callback,
            target_index=target_index,
        )
    elif category == StorageCategoryEnum.video.value:
        crud = await get_crud_sync(
            protocol,
            storage_id,
            is_progress=progress,
            callback=video_callback,
            target_index=target_index,
        )
    await crud.sync()

    tf = time.time()
    td = tf - ti
    print(f"total time: {td}(s)")
