from back.settings import setting
from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

title = setting.app_title

favicon_url = setting.app_favicon

swagger_js_url = setting.app_docs_swagger_js_url
swagger_css_url = setting.app_docs_swagger_css_url
redoc_js_url = setting.app_docs_redoc_js_url


router = APIRouter()


@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        swagger_js_url=swagger_js_url,
        swagger_css_url=swagger_css_url,
        title=title,
        swagger_favicon_url=favicon_url,
    )


@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=title,
        redoc_js_url=redoc_js_url,
        redoc_favicon_url=favicon_url,
    )
