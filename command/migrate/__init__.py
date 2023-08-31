import time
from enum import Enum

import typer
from elasticsearch import AsyncElasticsearch

from back.crud.async_sync import get_crud_sync
from back.model.base import SourceProtocolEnum
from back.settings import setting
from command.migrate.init.async_elasticsearch import create_gallery
from command.migrate.model.gallery import Gallery as NewGallery
from command.migrate.model.old_gallery import Gallery as OldGallery
from command.migrate.model.old_video import Video as OldVideo
from command.migrate.model.video import Video as NewVideo
from lib.typer import ZetsuBouTyper

_help = """
Migrate the data to the new version.
"""
app = ZetsuBouTyper(name="migrate", help=_help)

ELASTICSEARCH_URLS = setting.elastic_urls


class StorageCategoryEnum(str, Enum):
    gallery: str = "gallery"
    video: str = "video"


def gallery_callback(source: OldGallery) -> NewGallery:
    new_gallery = NewGallery()
    new_gallery.id = source.id
    new_gallery.path = source.path
    new_gallery.name = source.attributes.name
    new_gallery.raw_name = source.attributes.raw_name
    new_gallery.src = [source.attributes.src]

    new_gallery.last_updated = source.timestamp
    new_gallery.upload_date = source.mtime

    new_gallery.labels = source.labels
    new_gallery.tags = source.tags

    new_gallery.attributes.category = source.attributes.category
    new_gallery.attributes.rating = source.attributes.rating
    new_gallery.attributes.uploader = source.attributes.uploader
    new_gallery.attributes.pages = source.attributes.pages

    return new_gallery


def video_callback(source: OldVideo) -> NewVideo:
    new_video = NewVideo()
    new_video.id = source.id
    new_video.path = source.path
    new_video.name = source.name
    new_video.other_names = source.other_names
    new_video.src = source.attributes.src

    new_video.last_updated = source.timestamp

    new_video.attributes.category = source.attributes.category
    new_video.attributes.rating = source.attributes.rating
    new_video.attributes.uploader = source.attributes.uploader

    new_video.attributes.width = source.attributes.width
    new_video.attributes.height = source.attributes.height
    new_video.attributes.duration = source.attributes.duration
    new_video.attributes.fps = source.attributes.fps
    new_video.attributes.frames = source.attributes.frames
    new_video.attributes.md5 = source.attributes.md5

    return new_video


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
            new_model=NewGallery,
            target_index=target_index,
        )
    elif category == StorageCategoryEnum.video.value:
        crud = await get_crud_sync(
            protocol,
            storage_id,
            is_progress=progress,
            callback=video_callback,
            new_model=NewVideo,
            target_index=target_index,
        )
    await crud.sync()

    tf = time.time()
    td = tf - ti
    print(f"total time: {td}(s)")
