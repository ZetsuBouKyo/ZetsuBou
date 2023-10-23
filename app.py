import uvicorn
from elasticsearch.exceptions import NotFoundError, RequestError
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from minio.error import S3Error
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from back.api import router as api
from back.init.async_elasticsearch import init_indices
from back.init.async_storage import init_storage
from back.init.check import ping
from back.init.database import init_table
from back.init.route import router as init
from back.route import router as views
from back.settings import setting
from back.utils.exceptions import RequiresLoginException
from cli import app as cli_app  # noqa

APP_SECURITY = setting.app_security
TITLE = setting.app_title
HOST = setting.app_host
PORT = setting.app_port
FRONT = setting.app_front
FRONT_DOCS = setting.app_front_docs
STATICS = setting.app_statics

description = """
ZetsuBou is a web-based app to serve your own image galleries and make annotation
on your collections.

This is written in Python 3 and Vue 3.
"""


app = FastAPI(title=TITLE, description=description, docs_url=None, redoc_url=None)


app.mount("/docs", StaticFiles(directory=FRONT_DOCS, html=True), name="documentation")
app.mount("/assets", StaticFiles(directory=f"{FRONT}/assets"), name="assets")
app.mount("/statics", StaticFiles(directory=f"{STATICS}"), name="statics")


async def startup():
    are_services = await ping()
    if not are_services and not APP_SECURITY:
        app.include_router(init)
        return

    app.add_event_handler("startup", init_table)
    app.add_event_handler("startup", init_indices)
    app.add_event_handler("startup", init_storage)

    app.include_router(views)
    app.include_router(api, prefix="/api")


app.add_event_handler("startup", startup)


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse("/NotFound")


@app.exception_handler(Exception)
async def exception_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": exc.args})


@app.exception_handler(NotFoundError)
async def elasticsearch_not_found_error_handler():
    return JSONResponse(status_code=404, content={"detail": "Repo tag not found"})


@app.exception_handler(RequestError)
async def elasticsearch_request_error_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": exc.info})


@app.exception_handler(S3Error)
async def minio_s3error_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": exc.code})


@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: sqlalchemy {exc.code}"},
    )


@app.exception_handler(RequiresLoginException)
async def requires_login_exception_handler(request: Request, _: Exception):
    if request.url.path == "/":
        return RedirectResponse("/login")
    return RedirectResponse(f"/login?redirect={request.url.path}")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
