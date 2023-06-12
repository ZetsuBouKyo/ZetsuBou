from back.settings import setting
from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

TITLE = setting.app_title

FAVICON_URL = setting.app_favicon

SWAGGER_JS_URL = setting.app_docs_swagger_js_url
SWAGGER_CSS_URL = setting.app_docs_swagger_css_url
REDOC_JS_URL = setting.app_docs_redoc_js_url


router = APIRouter()


@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        swagger_js_url=SWAGGER_JS_URL,
        swagger_css_url=SWAGGER_CSS_URL,
        title=TITLE,
        swagger_favicon_url=FAVICON_URL,
    )


@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=TITLE,
        redoc_js_url=REDOC_JS_URL,
        redoc_favicon_url=FAVICON_URL,
    )
