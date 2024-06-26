from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from back.dependency.security import view_security
from back.model.elasticsearch import (
    ElasticsearchAnalyzerEnum,
    ElasticsearchQueryBooleanEnum,
)
from back.model.gallery import GalleryOrderedFieldEnum
from back.model.video import VideoOrderedFieldEnum
from back.settings import setting

FRONT = setting.app_front

router = APIRouter()
public_router = APIRouter()
private_router = APIRouter(dependencies=[view_security()])

templates = Jinja2Templates(directory=FRONT)


def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def table(request: Request, page: int = 1, size: int = None):
    return index(request)


@private_router.get("/")
async def root(
    request: Request,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = None,
    size: int = None,
    boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
):
    return index(request)


@private_router.get("/gallery/search")
async def gallery_search(
    request: Request,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = None,
    size: int = None,
    boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
):
    return index(request)


@private_router.get("/gallery/random")
async def gallery_random(
    request: Request,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = None,
    size: int = None,
    boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    seed: int = 1048596,
):
    return index(request)


@private_router.get("/gallery/advanced-search")
async def gallery_advanced_search(
    request: Request,
    page: int = 1,
    size: int = None,
    keywords: str = None,
    keywords_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    keywords_fuzziness: int = 0,
    keywords_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    name: str = None,
    name_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    name_fuzziness: int = 0,
    name_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    raw_name: str = None,
    raw_name_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    raw_name_fuzziness: int = 0,
    raw_name_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    src: str = None,
    src_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    src_fuzziness: int = 0,
    src_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    category: str = None,
    rating_gte: int = None,
    rating_lte: int = None,
    tag_field_1: str = None,
    tag_value_1: str = None,
    label_1: str = None,
    order_by: GalleryOrderedFieldEnum = None,
    is_desc: bool = True,
):
    return index(request)


private_router.add_api_route("/gallery", index)


@private_router.get("/video/search")
async def video_search(
    request: Request,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = None,
    size: int = None,
    boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
):
    return index(request)


@private_router.get("/video/random")
async def video_random(
    request: Request,
    keywords: str = "",
    page: int = 1,
    fuzziness: int = None,
    size: int = None,
    boolean: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    seed: int = 1048596,
):
    return index(request)


@private_router.get("/video/advanced-search")
async def video_advanced_search(
    request: Request,
    page: int = 1,
    size: int = None,
    keywords: str = None,
    keywords_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    keywords_fuzziness: int = 0,
    keywords_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    name: str = None,
    name_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    name_fuzziness: int = 0,
    name_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    other_names: str = None,
    other_names_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
    other_names_fuzziness: int = 0,
    other_names_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
    category: str = None,
    rating_gte: int = None,
    rating_lte: int = None,
    height_gte: int = None,
    height_lte: int = None,
    width_gte: int = None,
    width_lte: int = None,
    duration_gte: int = None,
    duration_lte: int = None,
    tag_field_1: str = None,
    tag_value_1: str = None,
    label_1: str = None,
    order_by: VideoOrderedFieldEnum = None,
    is_desc: bool = True,
):
    return index(request)


private_router.add_api_route("/initialization", index)

private_router.add_api_route("/bookmark", index)
private_router.add_api_route("/bookmark/gallery", table)
private_router.add_api_route("/bookmark/video", table)

private_router.add_api_route("/settings", index)
private_router.add_api_route("/settings/account", index)
private_router.add_api_route("/settings/appearance", index)
private_router.add_api_route("/settings/authentication", index)
private_router.add_api_route("/settings/storage-minio", table)
private_router.add_api_route("/settings/system", index)

private_router.add_api_route("/settings/elasticsearch-count", table)
private_router.add_api_route("/settings/elasticsearch-search", table)

private_router.add_api_route("/settings/tag", table)
private_router.add_api_route("/settings/tag-token", table)
private_router.add_api_route("/settings/tag-attribute", table)
private_router.add_api_route("/settings/tag-front-ui", index)

private_router.add_api_route("/settings/quest", table)
private_router.add_api_route("/settings/elasticsearch-count-quest", table)

private_router.add_api_route("/settings/users", table)
private_router.add_api_route("/settings/group", table)

private_router.add_api_route("/video", index)

private_router.add_api_route("/g/{gallery_id}", index)
private_router.add_api_route("/g/{gallery_id}/i/{image}", index)

private_router.add_api_route("/v/{video_id}", index)

public_router.add_api_route("/construction", index)
public_router.add_api_route("/NotFound", index, tags=["Exception"])


@public_router.get("/login")
async def login(request: Request, redirect: str = None):
    return index(request)


router.include_router(public_router)
router.include_router(private_router)
