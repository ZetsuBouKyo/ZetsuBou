from operator import ge, le
from typing import Any, Callable, Dict, List, Tuple, Union

import pytest

from back.crud.async_elasticsearch import ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW
from back.crud.async_gallery import (
    ELASTICSEARCH_SIZE,
    CrudAsyncElasticsearchGallery,
    get_gallery_by_gallery_id,
)
from back.model.elasticsearch import (
    ElasticsearchAnalyzerEnum,
    ElasticsearchQueryBooleanEnum,
)
from back.model.gallery import Galleries, Gallery, GalleryOrderedFieldEnum
from back.settings import setting
from back.utils.dt import iso2datetime
from lib.faker.gallery import galleries
from lib.faker.tag import TagCategoryEnum, TagCountryEnum, TagEnum, TagLanguageEnum
from tests.general.logging import logger
from tests.general.session import (
    Nested20200GalleryIntegrationSession,
    SimpleGalleryIntegrationSession,
)
from tests.general.summary import print_divider

STORAGE_TESTS_GALLERIES = setting.storage_tests_galleries


def is_faker_gallery(faker_gallery: Gallery, elasticsearch_gallery: Gallery) -> bool:
    faker_gallery.other_names.sort()
    faker_gallery.src.sort()
    faker_gallery.labels.sort()
    elasticsearch_gallery.other_names.sort()
    elasticsearch_gallery.src.sort()
    elasticsearch_gallery.labels.sort()
    for field in faker_gallery.tags.keys():
        faker_gallery.tags[field].sort()
        if field not in elasticsearch_gallery.tags:
            return False
        elasticsearch_gallery.tags[field].sort()
    if (
        faker_gallery.name == elasticsearch_gallery.name
        and faker_gallery.raw_name == elasticsearch_gallery.raw_name
        and faker_gallery.other_names == elasticsearch_gallery.other_names
        and faker_gallery.src == elasticsearch_gallery.src
        and faker_gallery.labels == elasticsearch_gallery.labels
        and faker_gallery.tags == elasticsearch_gallery.tags
        and faker_gallery.attributes.category
        == elasticsearch_gallery.attributes.category
        and faker_gallery.attributes.rating == elasticsearch_gallery.attributes.rating
        and faker_gallery.attributes.uploader
        == elasticsearch_gallery.attributes.uploader
        and faker_gallery.attributes.pages == elasticsearch_gallery.attributes.pages
    ):
        return True
    return False


def assert_gallery(docs: dict, arg: Tuple[Gallery]):
    galleries = Galleries(**docs)
    faker_gallery = arg[0]
    for g in galleries.hits.hits:
        if is_faker_gallery(faker_gallery, g.source):
            break
    else:
        assert False, galleries


def assert_eq_0(docs: dict, *_):
    galleries = Galleries(**docs)
    assert len(galleries.hits.hits) == 0


def assert_ge_0(docs: dict, *_):
    galleries = Galleries(**docs)
    assert len(galleries.hits.hits) > 0


def assert_default_sorting(docs: dict, *_):
    galleries = Galleries(**docs)
    total = len(galleries.hits.hits)
    assert total > 1
    last = iso2datetime(galleries.hits.hits[0].source.last_updated)
    for i in range(1, total):
        current = iso2datetime(galleries.hits.hits[i].source.last_updated)
        assert last > current
        last = current


def assert_include_tag_value(docs: dict, args: Tuple[str, str]):
    galleries = Galleries(**docs)
    tag_field = args[0]
    tag_field_value = args[1]

    assert len(galleries.hits.hits) > 0

    for doc in galleries.hits.hits:
        gallery = doc.source
        assert gallery.tags.get(tag_field, None) is not None, doc
        assert tag_field_value in gallery.tags[tag_field], doc


def assert_exclude_tag_value(docs: dict, args: Tuple[str, str]):
    galleries = Galleries(**docs)
    tag_field = args[0]
    tag_field_value = args[1]

    for doc in galleries.hits.hits:
        gallery = doc.source
        if gallery.tags.get(tag_field, None) is None:
            continue
        assert tag_field_value not in gallery.tags[tag_field], doc


def assert_exclude_tag_field(docs: dict, args: Tuple[str]):
    galleries = Galleries(**docs)
    tag_field = args[0]

    for doc in galleries.hits.hits:
        gallery = doc.source
        if gallery.tags.get(tag_field, None) is not None:
            assert False, doc


def assert_rating_sorting(
    docs: dict,
    arg: Tuple[Callable[[Union[float, int], Union[float, int]], bool]],
):
    galleries = Galleries(**docs)
    operator = arg[0]
    total = len(galleries.hits.hits)
    assert total > 1
    last = galleries.hits.hits[0].source.attributes.rating
    for i in range(1, total):
        current = galleries.hits.hits[i].source.attributes.rating
        if current is None:
            continue
        assert operator(last, current), galleries.hits.hits[i]
        last = current


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_gallery_by_gallery_id():
    async with SimpleGalleryIntegrationSession() as session:
        gallery = session.galleries[0]
        gallery_by_es = await get_gallery_by_gallery_id(gallery.id)

        assert gallery.id == gallery_by_es.id
        assert gallery.name == gallery_by_es.name


@pytest.mark.parametrize(
    (
        "assert_function",
        "assert_function_args",
        "page",
        "size",
        "keywords",
        "keywords_analyzer",
        "keywords_fuzziness",
        "keywords_bool",
        "name",
        "name_analyzer",
        "name_fuzziness",
        "name_bool",
        "raw_name",
        "raw_name_analyzer",
        "raw_name_fuzziness",
        "raw_name_bool",
        "other_names",
        "other_names_analyzer",
        "other_names_fuzziness",
        "other_names_bool",
        "src",
        "src_analyzer",
        "src_fuzziness",
        "src_bool",
        "path",
        "path_analyzer",
        "path_fuzziness",
        "path_bool",
        "category",
        "uploader",
        "rating_gte",
        "rating_lte",
        "order_by",
        "is_desc",
        "labels",
        "tags",
    ),
    [
        # default
        (
            assert_ge_0,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            None,  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # keywords_bool
            None,  # name
            ElasticsearchAnalyzerEnum.DEFAULT,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # name_bool
            None,  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # raw_name_bool
            None,  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # other_names_bool
            None,  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # src_bool
            None,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # path_bool
            None,  # category
            None,  # uploader
            None,  # rating_gte
            None,  # rating_lte
            None,  # order_by
            True,  # is_desc
            [],  # labels
            {},  # tags
        ),
        # string enum
        (
            assert_ge_0,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            "",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT.value,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD.value,  # keywords_bool
            "",  # name
            ElasticsearchAnalyzerEnum.DEFAULT.value,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD.value,  # name_bool
            None,  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # raw_name_bool
            None,  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # other_names_bool
            None,  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # src_bool
            None,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # path_bool
            None,  # category
            None,  # uploader
            None,  # rating_gte
            None,  # rating_lte
            None,  # order_by
            True,  # is_desc
            [],  # labels
            {},  # tags
        ),
        # fuzziness, range, boolean, labels, and tags
        (
            assert_gallery,  # assert_function
            (galleries[0],),  # assert_function_args
            1,  # page
            10,  # size
            "中",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keywords_analyzer
            1,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # keywords_bool
            "Zhonghu",  # name
            ElasticsearchAnalyzerEnum.DEFAULT,  # name_analyzer
            1,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # name_bool
            "中",  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            1,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # raw_name_bool
            "章",  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            1,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # other_names_bool
            "唐詩三百首",  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            1,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # src_bool
            STORAGE_TESTS_GALLERIES,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            1,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # path_bool
            TagCategoryEnum.BOOK.value,  # category
            TagEnum.ZETSUBOUKYO.value,  # uploader
            4,  # rating_gte
            4,  # rating_lte
            None,  # order_by
            True,  # is_desc
            [TagLanguageEnum.CHINESE.value],  # labels
            {TagCategoryEnum.COUNTRY.value: [TagCountryEnum.TAIWAN.value]},  # tags
        ),
        # ngram, range, boolean, labels, and tags
        (
            assert_gallery,  # assert_function
            (galleries[0],),  # assert_function_args
            1,  # page
            10,  # size
            "中",  # keywords
            ElasticsearchAnalyzerEnum.NGRAM,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # keywords_bool
            "Zhonghua",  # name
            ElasticsearchAnalyzerEnum.NGRAM,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # name_bool
            "中文",  # raw_name
            ElasticsearchAnalyzerEnum.NGRAM,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # raw_name_bool
            "章福記書局",  # other_names
            ElasticsearchAnalyzerEnum.NGRAM,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # other_names_bool
            "唐",  # src
            ElasticsearchAnalyzerEnum.NGRAM,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # src_bool
            STORAGE_TESTS_GALLERIES[0],  # path
            ElasticsearchAnalyzerEnum.NGRAM,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # path_bool
            None,  # category
            None,  # uploader
            4,  # rating_gte
            4,  # rating_lte
            None,  # order_by
            True,  # is_desc
            [TagLanguageEnum.CHINESE.value],  # labels
            {TagCategoryEnum.COUNTRY.value: [TagCountryEnum.TAIWAN.value]},  # tags
        ),
        (
            assert_gallery,  # assert_function
            (galleries[2],),  # assert_function_args
            1,  # page
            10,  # size
            "vol",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # keywords_bool
            None,  # name
            ElasticsearchAnalyzerEnum.DEFAULT,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # name_bool
            None,  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # raw_name_bool
            None,  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # other_names_bool
            None,  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # src_bool
            None,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # path_bool
            None,  # category
            None,  # uploader
            None,  # rating_gte
            None,  # rating_lte
            None,  # order_by
            True,  # is_desc
            [],  # labels
            {},  # tags
        ),
        (
            assert_default_sorting,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            TagLanguageEnum.ENGLISH.value,  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # keywords_bool
            None,  # name
            ElasticsearchAnalyzerEnum.DEFAULT,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # name_bool
            None,  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # raw_name_bool
            None,  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # other_names_bool
            None,  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # src_bool
            None,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # path_bool
            None,  # category
            None,  # uploader
            None,  # rating_gte
            None,  # rating_lte
            None,  # order_by
            True,  # is_desc
            [],  # labels
            {},  # tags
        ),
        (
            assert_rating_sorting,  # assert_function
            (ge,),  # assert_function_args
            1,  # page
            10,  # size
            TagLanguageEnum.ENGLISH.value,  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # keywords_bool
            None,  # name
            ElasticsearchAnalyzerEnum.DEFAULT,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # name_bool
            None,  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # raw_name_bool
            None,  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # other_names_bool
            None,  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # src_bool
            None,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # path_bool
            None,  # category
            None,  # uploader
            None,  # rating_gte
            None,  # rating_lte
            GalleryOrderedFieldEnum.RATING.value,  # order_by
            True,  # is_desc
            [],  # labels
            {},  # tags
        ),
        (
            assert_rating_sorting,  # assert_function
            (le,),  # assert_function_args
            1,  # page
            10,  # size
            TagLanguageEnum.ENGLISH.value,  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keywords_analyzer
            0,  # keywords_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # keywords_bool
            None,  # name
            ElasticsearchAnalyzerEnum.DEFAULT,  # name_analyzer
            0,  # name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # name_bool
            None,  # raw_name
            ElasticsearchAnalyzerEnum.DEFAULT,  # raw_name_analyzer
            0,  # raw_name_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # raw_name_bool
            None,  # other_names
            ElasticsearchAnalyzerEnum.DEFAULT,  # other_names_analyzer
            0,  # other_names_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # other_names_bool
            None,  # src
            ElasticsearchAnalyzerEnum.URL,  # src_analyzer
            0,  # src_fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # src_bool
            None,  # path
            ElasticsearchAnalyzerEnum.URL,  # path_analyzer
            0,  # path_fuzziness
            ElasticsearchQueryBooleanEnum.MUST,  # path_bool
            None,  # category
            None,  # uploader
            None,  # rating_gte
            None,  # rating_lte
            GalleryOrderedFieldEnum.RATING.value,  # order_by
            False,  # is_desc
            [],  # labels
            {},  # tags
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_advanced_search(
    assert_function: Callable[[dict, Tuple[Any]], None],
    assert_function_args: Tuple[Any, ...],
    page: int,
    size: int,
    keywords: str,
    keywords_analyzer: ElasticsearchAnalyzerEnum,
    keywords_fuzziness: int,
    keywords_bool: ElasticsearchQueryBooleanEnum,
    name: str,
    name_analyzer: ElasticsearchAnalyzerEnum,
    name_fuzziness: int,
    name_bool: ElasticsearchQueryBooleanEnum,
    raw_name: str,
    raw_name_analyzer: ElasticsearchAnalyzerEnum,
    raw_name_fuzziness: int,
    raw_name_bool: ElasticsearchQueryBooleanEnum,
    other_names: str,
    other_names_analyzer: ElasticsearchAnalyzerEnum,
    other_names_fuzziness: int,
    other_names_bool: ElasticsearchQueryBooleanEnum,
    src: str,
    src_analyzer: ElasticsearchAnalyzerEnum,
    src_fuzziness: int,
    src_bool: ElasticsearchQueryBooleanEnum,
    path: str,
    path_analyzer: ElasticsearchAnalyzerEnum,
    path_fuzziness: int,
    path_bool: ElasticsearchQueryBooleanEnum,
    category: str,
    uploader: str,
    rating_gte: int,
    rating_lte: int,
    order_by: GalleryOrderedFieldEnum,
    is_desc: bool,
    labels: List[str],
    tags: Dict[str, List[str]],
):
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            docs = await crud.advanced_search(
                page=page,
                size=size,
                keywords=keywords,
                keywords_analyzer=keywords_analyzer,
                keywords_fuzziness=keywords_fuzziness,
                keywords_bool=keywords_bool,
                name=name,
                name_analyzer=name_analyzer,
                name_fuzziness=name_fuzziness,
                name_bool=name_bool,
                raw_name=raw_name,
                raw_name_analyzer=raw_name_analyzer,
                raw_name_fuzziness=raw_name_fuzziness,
                raw_name_bool=raw_name_bool,
                other_names=other_names,
                other_names_analyzer=other_names_analyzer,
                other_names_fuzziness=other_names_fuzziness,
                other_names_bool=other_names_bool,
                src=src,
                src_analyzer=src_analyzer,
                src_fuzziness=src_fuzziness,
                src_bool=src_bool,
                path=path,
                path_analyzer=path_analyzer,
                path_fuzziness=path_fuzziness,
                path_bool=path_bool,
                category=category,
                uploader=uploader,
                rating_gte=rating_gte,
                rating_lte=rating_lte,
                order_by=order_by,
                is_desc=is_desc,
                labels=labels,
                tags=tags,
            )

            assert_function(docs, assert_function_args)


@pytest.mark.parametrize(
    ("page", "size", "keywords", "keyword_analyzer", "fuzziness", "boolean", "seed"),
    [
        (
            1,
            10,
            "",
            ElasticsearchAnalyzerEnum.DEFAULT,
            0,
            ElasticsearchQueryBooleanEnum.SHOULD,
            1048596,
        ),
        (
            1,
            10,
            TagLanguageEnum.ENGLISH.value,
            ElasticsearchAnalyzerEnum.DEFAULT,
            0,
            ElasticsearchQueryBooleanEnum.SHOULD,
            1048596,
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_random(
    page: int,
    size: int,
    keywords: str,
    keyword_analyzer: ElasticsearchAnalyzerEnum,
    fuzziness: int,
    boolean: ElasticsearchQueryBooleanEnum,
    seed: int,
):
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            docs = await crud.random(
                page,
                size=size,
                keywords=keywords,
                keyword_analyzer=keyword_analyzer,
                fuzziness=fuzziness,
                boolean=boolean,
                seed=seed,
            )
            assert_ge_0(docs)


@pytest.mark.parametrize(
    (
        "assert_function",
        "assert_function_args",
        "page",
        "size",
        "keywords",
        "keyword_analyzer",
        "fuzziness",
        "boolean",
    ),
    [
        # equivalent to match_all
        (
            assert_ge_0,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            "",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # boolean
        ),
        # keyword string enum
        (
            assert_ge_0,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            "TagLanguageEnum.ENGLISH.value",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT.value,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD.value,  # boolean
        ),
        # ngram
        (
            assert_ge_0,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            TagLanguageEnum.ENGLISH.value[0],  # keywords
            ElasticsearchAnalyzerEnum.NGRAM,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # boolean
        ),
        # keyword grammar: include the tag value
        (
            assert_include_tag_value,  # assert_function
            (
                TagCategoryEnum.COUNTRY.value,
                TagCountryEnum.TAIWAN.value,
            ),  # assert_function_args
            1,  # page
            10,  # size
            f"tags.{TagCategoryEnum.COUNTRY.value}={TagCountryEnum.TAIWAN.value}",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # boolean
        ),
        # keyword grammar: elasticsearch field does not exist
        (
            assert_ge_0,  # assert_function
            (),  # assert_function_args
            1,  # page
            10,  # size
            f"tags.{TagCategoryEnum.COUNTRY.value}={TagCountryEnum.TAIWAN.value} wrong=text",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # boolean
        ),
        # keyword grammar: exclude the tag value
        (
            assert_exclude_tag_value,  # assert_function
            (
                TagCategoryEnum.COUNTRY.value,
                TagCountryEnum.TAIWAN.value,
            ),  # assert_function_args
            1,  # page
            10,  # size
            f"-tags.{TagCategoryEnum.COUNTRY.value}={TagCountryEnum.TAIWAN.value}",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # boolean
        ),
        # keyword grammar: exclude the tag field
        (
            assert_exclude_tag_field,  # assert_function
            (TagCategoryEnum.COUNTRY.value,),  # assert_function_args
            1,  # page
            10,  # size
            f"-tags.{TagCategoryEnum.COUNTRY.value}",  # keywords
            ElasticsearchAnalyzerEnum.DEFAULT,  # keyword_analyzer
            0,  # fuzziness
            ElasticsearchQueryBooleanEnum.SHOULD,  # boolean
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_match(
    assert_function: Callable[[dict, Tuple[Any]], None],
    assert_function_args: Tuple[Any, ...],
    page: int,
    size: int,
    keywords: str,
    keyword_analyzer: ElasticsearchAnalyzerEnum,
    fuzziness: int,
    boolean: ElasticsearchQueryBooleanEnum,
):
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            docs = await crud.match(
                page,
                size=size,
                keywords=keywords,
                keyword_analyzer=keyword_analyzer,
                fuzziness=fuzziness,
                boolean=boolean,
            )
            assert_function(docs, assert_function_args)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_match_max_result_window():
    keywords = ""
    keyword_analyzer = ElasticsearchAnalyzerEnum.DEFAULT
    fuzziness = 0
    boolean = ElasticsearchQueryBooleanEnum.SHOULD
    async with Nested20200GalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            total = await crud.get_total()
            logger.info(f"total: {total}")
            assert total > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW, f"total: {total}"

            size = (total - ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW) // 3
            logger.info(f"size: {size}")
            assert size > 0, f"size: {size}"

            page = ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW // size + 1
            logger.info(f"page: {page}")
            assert total > size * page > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW
            assert total > size * (page + 1) > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW
            assert size * (page + 4) > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW

            docs = await crud.match(
                page + 1,
                size=size,
                keywords=keywords,
                keyword_analyzer=keyword_analyzer,
                fuzziness=fuzziness,
                boolean=boolean,
            )
            assert_ge_0(docs)

            docs = await crud.match(
                page + 4,
                size=size,
                keywords=keywords,
                keyword_analyzer=keyword_analyzer,
                fuzziness=fuzziness,
                boolean=boolean,
            )
            assert_eq_0(docs)

            print_divider()

            size = ELASTICSEARCH_SIZE
            logger.info(f"size: {size}")

            page = (ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW // size + 1) * 2
            logger.info(f"page: {page}")
            assert total > page * size > ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW * 2 + 1

            docs = await crud.match(
                page,
                size=size,
                keywords=keywords,
                keyword_analyzer=keyword_analyzer,
                fuzziness=fuzziness,
                boolean=boolean,
            )
            assert_ge_0(docs)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_match_by_query():
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            dsl = {"query": {"match_all": {}}}
            docs = await crud.match_by_query(dsl, 1)
            assert_ge_0(docs)


@pytest.mark.asyncio(scope="session")
async def test_match_phrase_prefix():
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            await crud.match_phrase_prefix("")


@pytest.mark.asyncio(scope="session")
async def test_iter():
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            c = 0
            async for _ in crud.iter(1000):
                c += 1
            logger.info(f"count: {c}")
            total = await crud.get_total()
            logger.info(f"total: {total}")

            assert c == total


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_custom():
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            dsl = {"query": {"match_all": {}}}
            docs = await crud.custom(dsl)
            logger.debug(f"query: {dsl}")
            logger.debug(f"docs: {docs}")


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_count():
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            dsl = {"query": {"match_all": {}}}
            total = await crud.count(dsl)
            logger.debug(f"query: {dsl}")
            logger.debug(f"count: {total.count}")


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_total():
    async with SimpleGalleryIntegrationSession():
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            total = await crud.get_total()
            assert total > 0


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_sources_by_ids():
    async with SimpleGalleryIntegrationSession() as session:
        galleries = session.galleries
        gallery_ids = [g.id for g in galleries]
        async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
            docs = await crud.get_sources_by_ids(gallery_ids)

            galleries = Galleries(**docs)
            assert len(galleries.hits.hits) == len(gallery_ids)

            gallery_elasticsearch_ids = [h.source.id for h in galleries.hits.hits]
            assert set(gallery_elasticsearch_ids) == set(gallery_ids)
