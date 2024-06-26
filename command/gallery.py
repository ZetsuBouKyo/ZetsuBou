import shutil
from pathlib import Path

import typer
from rich import print_json

from back.crud.async_gallery import (
    CrudAsyncElasticsearchGallery,
    CrudAsyncGallery,
    get_gallery_by_gallery_id,
)
from back.model.elasticsearch import (
    ElasticsearchAnalyzerEnum,
    ElasticsearchQueryBooleanEnum,
)
from back.settings import setting
from lib.typer import ZetsuBouTyper

ELASTICSEARCH_SIZE = setting.elastic_size
ELASTICSEARCH_INDEX_GALLERY = setting.elastic_index_gallery

GALLERY_DIR_FNAME = setting.gallery_dir_fname
GALLERY_TAG_FNAME = setting.gallery_tag_fname

_help = """
Manipulate the Galleries.
"""
app = ZetsuBouTyper(name="gallery", help=_help)


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
        gallery_tag_home_path = gallery_path / GALLERY_DIR_FNAME
        gallery_tag_path = gallery_tag_home_path / GALLERY_TAG_FNAME
        gallery_tag_path = str(gallery_tag_path)
        new_gallery_tag_path = gallery_tag_home_path / fname
        new_gallery_tag_path = str(new_gallery_tag_path)
        shutil.copy(gallery_tag_path, new_gallery_tag_path)


@app.command()
async def get_gallery_tag(gallery_id: str = typer.Argument(..., help="Gallery ID.")):
    """
    Get the gallery tag.
    """
    async with CrudAsyncElasticsearchGallery(
        is_from_setting_if_none=True
    ) as crud_elastic:
        elastic_gallery = await crud_elastic.get_by_id(gallery_id)
        print("Gallery from Elasticsearch")
        print_json(data=elastic_gallery.model_dump())

    async with CrudAsyncGallery(gallery_id, is_from_setting_if_none=True) as crud:
        storage_gallery = await crud.get_gallery_tag_from_storage()
        print("Gallery from Storage")
        print_json(data=storage_gallery.model_dump())


@app.command()
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
    boolean: ElasticsearchQueryBooleanEnum = typer.Option(
        default=ElasticsearchQueryBooleanEnum.SHOULD.value,
        help="The relation between keywords.",
    ),
    analyzer: ElasticsearchAnalyzerEnum = typer.Option(
        default=ElasticsearchAnalyzerEnum.DEFAULT.value,
        help="See Elasticsearch analyzer (https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html).",  # noqa
    ),
):
    """
    Search.
    """
    async with CrudAsyncElasticsearchGallery(
        index=index, is_from_setting_if_none=True
    ) as crud:
        resp = await crud.match(
            page,
            size=size,
            keywords=keywords,
            keyword_analyzer=analyzer,
            fuzziness=fuzziness,
            boolean=boolean,
        )
        resp.print()


@app.command()
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
    boolean: ElasticsearchQueryBooleanEnum = typer.Option(
        default=ElasticsearchQueryBooleanEnum.SHOULD.value,
        help="The relation between keywords.",
    ),
    analyzer: ElasticsearchAnalyzerEnum = typer.Option(
        default=ElasticsearchAnalyzerEnum.DEFAULT.value,
        help="See Elasticsearch analyzer (https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html).",  # noqa
    ),
    seed: int = typer.Option(default=1048596, help="Random seed."),
):
    """
    Random search.
    """
    async with CrudAsyncElasticsearchGallery(
        index=index, is_from_setting_if_none=True
    ) as crud:
        resp = await crud.random(
            page,
            size=size,
            keywords=keywords,
            keyword_analyzer=analyzer,
            fuzziness=fuzziness,
            boolean=boolean,
            seed=seed,
        )
        resp.print()


@app.command()
async def get_image_filenames(
    gallery_id: str = typer.Argument(..., help="Gallery ID.")
):
    """
    List the images in the gallery.
    """
    async with CrudAsyncGallery(gallery_id, is_from_setting_if_none=True) as crud:
        resp = await crud.get_image_filenames()
        print_json(data=resp)


@app.command()
async def update_gallery_tag(
    gallery_id: str = typer.Argument(..., help="Gallery ID."),
    name: str = typer.Option(default=None, help="Gallery name."),
    raw_name: str = typer.Option(default=None, help="Gallery raw name."),
    labels: str = typer.Option(default=None, help="Gallery labels."),
    label_separator: str = typer.Option(default=",", help="Gallery label separator."),
):
    """
    Update the gallery tag.
    """
    gallery = await get_gallery_by_gallery_id(gallery_id)
    print_json(data=gallery.model_dump())
    if name is not None:
        gallery.name = name
    if raw_name is not None:
        gallery.raw_name = raw_name
    if labels is not None:
        _labels = labels.split(label_separator)
        gallery.labels = _labels
        gallery.labels.sort()

    crud_async_gallery = CrudAsyncGallery(gallery_id, is_from_setting_if_none=True)
    await crud_async_gallery.init()
    await crud_async_gallery.update(gallery)
    print_json(data=gallery.model_dump())


@app.command()
async def delete(gallery_id: str = typer.Argument(..., help="Gallery ID.")):
    """
    Delete the gallery.
    """
    crud_async_gallery = CrudAsyncGallery(gallery_id, is_from_setting_if_none=True)
    await crud_async_gallery.init()
    await crud_async_gallery.delete()
