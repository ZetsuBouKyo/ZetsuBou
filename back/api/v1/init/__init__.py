from typing import Dict

from fastapi import APIRouter

from back.dependency.security import api_security
from back.init.check import check_host_port
from back.init.statics import get_static_file
from back.model.scope import ScopeEnum

from .ping import router as ping

PORTS = [5430, 5431, 5555, 6379, 6380, 8080, 9000, 9001, 9200]


router = APIRouter(prefix="/init")

router.include_router(ping)


@router.get(
    "/check-host-ports",
    response_model=Dict[int, bool],
    dependencies=[api_security([ScopeEnum.init_check_host_ports_get.value])],
)
def check_host_ports() -> Dict[int, bool]:
    host_ports = {}
    for port in PORTS:
        is_port = not check_host_port(port)
        host_ports[port] = is_port

    return host_ports


@router.get(
    "/download-redoc",
    dependencies=[api_security([ScopeEnum.init_download_redoc_get.value])],
)
async def download_redoc():
    redoc_url = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    redoc_map_url = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js.map"
    )

    await get_static_file(redoc_url)
    await get_static_file(redoc_map_url)


@router.get(
    "/download-swagger",
    dependencies=[api_security([ScopeEnum.init_download_swagger_get.value])],
)
async def download_swagger():
    swagger_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js"
    swagger_map_url = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js.map"
    )

    swagger_css_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css"
    swagger_css_map_url = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css.map"
    )

    await get_static_file(swagger_url)
    await get_static_file(swagger_map_url)
    await get_static_file(swagger_css_url)
    await get_static_file(swagger_css_map_url)
