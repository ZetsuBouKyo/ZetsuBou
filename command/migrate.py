from urllib.parse import urlparse

import typer
from elasticsearch.helpers import async_bulk

from back.crud.async_video import CrudAsyncElasticsearchVideo
from back.model.video import Video
from back.session.async_elasticsearch import async_elasticsearch
from lib.typer import ZetsuBouTyper

_help = """
Migrate the data to the new version.
"""
app = ZetsuBouTyper(name="migrate", help=_help)


@app.command()
async def video(index: str = typer.Argument(..., help="Video index name.")):
    """
    Change the format of the `path` in video tag.

    From `minio://{bucket name}/{prefix}` to `minio-{number}://{bucket name}/{prefix}`.
    """
    batch_size = 300
    crud = CrudAsyncElasticsearchVideo(
        size=300, index=index, is_from_setting_if_none=True
    )

    async for resp in crud.iter():
        batches = []
        for hit in resp.hits.hits:
            source = hit.source
            video = Video(**source)

            video_path = video.path
            video_url = urlparse(video_path)
            if video_url.scheme[5] == "-":
                continue

            id = int(video_url.scheme[5:])
            new_path = f"minio-{id}://{video_url.netloc}{video_url.path}"
            video.path = new_path

            print(new_path)
            action = {"_index": index, "_id": video.id, "_source": video.dict()}
            batches.append(action)
            if len(batches) == batch_size:
                await async_bulk(async_elasticsearch, batches)
                batches = []
        if len(batches) > 0:
            await async_bulk(async_elasticsearch, batches)
