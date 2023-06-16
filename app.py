import uvicorn
from elasticsearch.exceptions import NotFoundError, RequestError
from fastapi import FastAPI, HTTPException, Request
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
from back.init.logger import init_loggers
from back.init.route import router as init
from back.route import router as views
from back.settings import setting
from back.utils.exceptions import RequiresLoginException
from cli import app as cli_app  # noqa

TITLE = setting.app_title
HOST = setting.app_host
PORT = setting.app_port
FRONT = setting.app_front
STATICS = setting.app_statics

description = """
ZetsuBou is a web-based app to serve your own image galleries and make annotation
on your collections.

This is written in Python 3 and Vue 3.
"""

init_loggers()

app = FastAPI(title=TITLE, description=description, docs_url=None, redoc_url=None)

app.mount("/statics", StaticFiles(directory=f"{STATICS}"), name="statics")
app.mount("/assets", StaticFiles(directory=f"{FRONT}/assets"), name="assets")


async def startup():
    are_services = await ping()
    if not are_services:
        app.include_router(init)
    else:
        app.add_event_handler("startup", init_table)
        app.add_event_handler("startup", init_indices)
        app.add_event_handler("startup", init_storage)

        app.include_router(views)
        app.include_router(api, prefix="/api")


app.add_event_handler("startup", startup)


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: Exception):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse("/NotFound")


@app.exception_handler(HTTPException)
async def fastapi_http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(NotFoundError)
async def elastic_not_found_error(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"detail": "Repo tag not found"})


@app.exception_handler(RequestError)
async def elastic_request_error(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": exc.info})


@app.exception_handler(S3Error)
async def minio_s3error(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": exc.code})


@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: sqlalchemy {exc.code}"},
    )


@app.exception_handler(RequiresLoginException)
async def requires_login_exception(request: Request, exc: Exception):
    if request.url.path == "/":
        return RedirectResponse("/login")
    return RedirectResponse(f"/login?redirect={request.url.path}")


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
