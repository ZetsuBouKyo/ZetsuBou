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
from back.route import router as views
from back.session.elastic import init_index
from back.session.init_db import init_table
from back.session.minio import init_minio
from back.settings import setting
from back.utils.exceptions import RequiresLoginException
from cli import app as cli_app  # noqa

title = setting.app_title
host = setting.app_host
port = setting.app_port
front = setting.app_front
statics = setting.app_statics

description = """
ZetsuBou is a web-based app to serve your own image galleries and make annotation
on your collections.

This is written in Python 3 and Vue 3.
"""

app = FastAPI(title=title, description=description, docs_url=None, redoc_url=None)

app.add_event_handler("startup", init_table)
app.add_event_handler("startup", init_index)
app.add_event_handler("startup", init_minio)

app.mount("/statics", StaticFiles(directory=f"{statics}"), name="statics")
app.mount("/assets", StaticFiles(directory=f"{front}/assets"), name="assets")


app.include_router(views)
app.include_router(api, prefix="/api")


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: Exception):
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
    uvicorn.run(app, host=host, port=port)
