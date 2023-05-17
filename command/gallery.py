import shutil
from pathlib import Path

import typer
from back.crud.gallery import (
    CrudAsyncElasticsearchGallery,
    CrudAsyncGallery,
    CrudAsyncStorageGallery,
    get_gallery_by_gallery_id,
)
from back.model.elastic import AnalyzerEnum, QueryBoolean
from back.model.gallery import Gallery
from back.session.storage import get_storage_session_by_source
from back.settings import setting
from rich import print_json

from command.utils import sync

ELASTICSEARCH_SIZE = setting.elastic_size
ELASTICSEARCH_INDEX_GALLERY = setting.elastic_index_gallery

_help = """
Manipulate the Galleries.
"""
app = typer.Typer(name="gallery", help=_help)


@app.command()
def clone_tags(
    home: str = typer.Argument(
        ..., help="The path for the upper layer of the galleries"
    ),
    fname: str = typer.Argument(..., help="The new file name of the gallery tag."),
):
    """
    Clone the gallery tag.

    Clone all gallery tags under home path with new file name. The new file is placed
     with the origin gallery tag under the same repository.
    """

    if home is None or fname is None:
        return
    home = Path(home)
    if not home.exists() or not home.is_dir():
        return

    for gallery_path in home.iterdir():
        gallery_tag_home_path = gallery_path / setting.gallery_dir_fname
        gallery_tag_path = gallery_tag_home_path / setting.gallery_tag_fname
        gallery_tag_path = str(gallery_tag_path)
        new_gallery_tag_path = gallery_tag_home_path / fname
        new_gallery_tag_path = str(new_gallery_tag_path)
        shutil.copy(gallery_tag_path, new_gallery_tag_path)


@app.command()
@sync
async def get_gallery_tag(gallery_id: str = typer.Argument(..., help="Gallery ID.")):
    crud = CrudAsyncElasticsearchGallery(is_from_setting_if_none=True)
    gallery_dict = await crud.get_source_by_id(gallery_id)
    gallery = Gallery(**gallery_dict)

    storage_session = await get_storage_session_by_source(gallery)
    crud = CrudAsyncStorageGallery(
        storage_session=storage_session, is_from_setting_if_none=True
    )
    gallery_tag = await crud.get_gallery_tag(gallery)
    print(gallery_tag)


@app.command()
@sync
async def match(
    page: int = typer.Argument(..., help="Page number."),
    index: str = typer.Option(
        default=ELASTICSEARCH_INDEX_GALLERY, help="Gallery index name."
    ),
    size: int = typer.Option(
        default=ELASTICSEARCH_SIZE, help="Number of returning results."
    ),
    keywords: str = typer.Option(default="", help="Keywords for searching."),
    fuzziness: int = typer.Option(
        default=0,
        help="See Elasticsearch fuzziness (https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness).",  # noqa
    ),
    boolean: QueryBoolean = typer.Option(
        default=QueryBoolean.SHOULD.value, help="The relation between keywords."
    ),
    analyzer: AnalyzerEnum = typer.Option(
        default=AnalyzerEnum.DEFAULT.value,
        help="See Elasticsearch analyzer (https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html).",  # noqa
    ),
):
    crud = CrudAsyncElasticsearchGallery(
        size=size, index=index, analyzer=analyzer, is_from_setting_if_none=True
    )
    resp = await crud.match(
        page, keywords=keywords, fuzziness=fuzziness, boolean=boolean
    )
    resp.print()


@app.command()
@sync
async def random(
    page: int = typer.Argument(..., help="Page number."),
    index: str = typer.Option(
        default=ELASTICSEARCH_INDEX_GALLERY, help="Gallery index name."
    ),
    size: int = typer.Option(
        default=ELASTICSEARCH_SIZE, help="Number of returning results."
    ),
    keywords: str = typer.Option(default="", help="Keywords for searching."),
    fuzziness: int = typer.Option(
        default=0,
        help="See Elasticsearch fuzziness (https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness).",  # noqa
    ),
    boolean: QueryBoolean = typer.Option(
        default=QueryBoolean.SHOULD.value, help="The relation between keywords."
    ),
    analyzer: AnalyzerEnum = typer.Option(
        default=AnalyzerEnum.DEFAULT.value,
        help="See Elasticsearch analyzer (https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html).",  # noqa
    ),
    seed: int = typer.Option(default=1048596, help="Random seed."),
):
    crud = CrudAsyncElasticsearchGallery(
        size=size, index=index, analyzer=analyzer, is_from_setting_if_none=True
    )
    resp = await crud.random(
        page, keywords=keywords, fuzziness=fuzziness, boolean=boolean, seed=seed
    )
    resp.print()


@app.command()
@sync
async def get_image_filenames(
    gallery_id: str = typer.Argument(..., help="Gallery ID.")
):
    gallery = await get_gallery_by_gallery_id(gallery_id)
    storage_session = await get_storage_session_by_source(gallery)
    crud = CrudAsyncStorageGallery(
        storage_session=storage_session, is_from_setting_if_none=True
    )
    resp = await crud.get_image_filenames(gallery)
    print_json(data=resp)


@app.command()
@sync
async def get_gallery_tag_in_storage(
    gallery_id: str = typer.Argument(..., help="Gallery ID.")
):
    gallery = await get_gallery_by_gallery_id(gallery_id)
    storage_session = await get_storage_session_by_source(gallery)
    crud = CrudAsyncStorageGallery(
        storage_session=storage_session, is_from_setting_if_none=True
    )
    resp = await crud.get_gallery_tag(gallery)
    print_json(data=resp.dict())


@app.command()
@sync
async def update_gallery_tag(
    gallery_id: str = typer.Argument(..., help="Gallery ID."),
    name: str = typer.Option(default=None, help="Gallery name."),
    raw_name: str = typer.Option(default=None, help="Gallery raw name."),
    labels: str = typer.Option(default=None, help="Gallery labels."),
    label_separator: str = typer.Option(default=",", help="Gallery label separator."),
):
    gallery = await get_gallery_by_gallery_id(gallery_id)
    print_json(data=gallery.dict())
    if name is not None:
        gallery.attributes.name = name
    if raw_name is not None:
        gallery.attributes.raw_name = raw_name
    if labels is not None:
        _labels = labels.split(label_separator)
        gallery.labels = _labels
        gallery.labels.sort()

    crud_async_gallery = CrudAsyncGallery(gallery_id, is_from_setting_if_none=True)
    await crud_async_gallery.init()
    await crud_async_gallery.update(gallery)
    print_json(data=gallery.dict())


@app.command()
@sync
async def delete(gallery_id: str = typer.Argument(..., help="Gallery ID.")):
    crud_async_gallery = CrudAsyncGallery(gallery_id, is_from_setting_if_none=True)
    await crud_async_gallery.init()
    await crud_async_gallery.delete()
