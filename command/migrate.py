from urllib.parse import urlparse

import typer
from back.crud.async_video import CrudAsyncElasticsearchVideo
from back.model.video import Video
from back.session.elasticsearch import elastic_client

from command.utils import sync
from elasticsearch import helpers

app = typer.Typer(name="migrate")


@app.command()
@sync
async def video(index: str = typer.Argument(..., help="Video index name.")):
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
                helpers.bulk(elastic_client, batches)
                batches = []
        if len(batches) > 0:
            helpers.bulk(elastic_client, batches)
