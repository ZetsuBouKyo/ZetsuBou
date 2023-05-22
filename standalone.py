import asyncio
import json
import os
import re
from pathlib import Path
from shutil import which
from uuid import uuid4

import requests
import uvicorn
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import FastAPI, HTTPException, Request
from minio import Minio
from pydantic import BaseModel, BaseSettings
from sqlalchemy import event
from sqlalchemy.engine import Engine
from starlette.responses import JSONResponse
from urllib3.exceptions import NewConnectionError

from back.db.model import StorageMinio
from back.model.base import SourceProtocolEnum
from back.model.gallery import Gallery
from back.schema.basic import Message
from back.settings import setting
from back.utils.dt import get_now

default_setting_path = Path("etc", "standalone.env")


class State(BaseModel):
    is_sync: bool = False


state = State()


class StandAloneSetting(BaseSettings):
    app_host: str = setting.app_host
    app_port: int = setting.app_port
    app_admin_email: str = setting.app_admin_email
    app_admin_password: str = setting.app_admin_password

    gallery_dir_fname: str = setting.gallery_dir_fname
    gallery_tag_fname: str = setting.gallery_tag_fname

    standalone_host: str = setting.standalone_host
    standalone_port: int = setting.standalone_port

    standalone_sync_galleries_from_path: str = None
    standalone_sync_galleries_to_path: str = None

    minio_user: str = None
    minio_password: str = None
    minio_endpoint: str = None
    minio_volume: str = None
    minio_is_secure: str = setting.minio_is_secure
    minio_storage_id: int = None

    @property
    def minio_secure(cls):
        if cls.minio_is_secure.lower() == "false":
            return False
        elif cls.minio_is_secure.lower() == "true":
            return True
        return False

    elastic_urls: str = setting.elastic_urls
    elastic_index_gallery: str = setting.elastic_index_gallery

    @property
    def elastic_hosts(cls):
        if not cls.elastic_urls:
            return []
        return cls.elastic_urls.split(",")


standalone_setting = StandAloneSetting(_env_file=str(default_setting_path))
host = standalone_setting.standalone_host
port = standalone_setting.standalone_port


elastic_hosts = standalone_setting.elastic_hosts
elastic_index_gallery = standalone_setting.elastic_index_gallery
elastic_client = Elasticsearch(hosts=elastic_hosts)

minio_volume = standalone_setting.minio_volume
minio_endpoint = standalone_setting.minio_endpoint
minio_secure = standalone_setting.minio_secure
minio_user = standalone_setting.minio_user
minio_password = standalone_setting.minio_password
minio_client = Minio(
    minio_endpoint,
    secure=minio_secure,
    access_key=minio_user,
    secret_key=minio_password,
)
minio_storage_id = standalone_setting.minio_storage_id


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


app = FastAPI()


def get_minio_path_by_gallery_id(gallery_id: str):
    res = elastic_client.get(index=elastic_index_gallery, id=gallery_id)
    return res["_source"]["path"]


async def open_folder(request: Request, gallery_id: str):
    minio_path = get_minio_path_by_gallery_id(gallery_id)
    # if request.client.host != host:
    #     raise HTTPException(status_code=409, detail="You are not at host server")

    if minio_volume is None:
        raise HTTPException(status_code=404, detail="'minio_volume' not found")

    relative_path = minio_path.split("//")[-1]
    if len(relative_path) > 0 and relative_path[0] == "/":
        raise HTTPException(
            status_code=409,
            detail=f"Path in Minio path after removing '{SourceProtocolEnum.MINIO.value}' should not start with '/'",  # noqa
        )

    path_at_host = Path(minio_volume, relative_path)
    print(path_at_host)

    preferred_app = "nautilus"
    if which(preferred_app) is not None:
        cmd = f'{preferred_app} "{str(path_at_host)}"'
        await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        return Message(detail="ok")
    return Message(detail=f"{preferred_app}: command not found")


@app.get("/open")
async def get_open_folder(request: Request, gallery_id: str):
    return await open_folder(request, gallery_id)


@app.options("/open")
async def options_open_folder(request: Request, gallery_id: str):
    return await open_folder(request, gallery_id)


app_host = standalone_setting.app_host
app_port = standalone_setting.app_port
app_root_url = f"http://{app_host}:{app_port}"


def get_token(username: str, password: str):
    files = {
        "username": (None, username),
        "password": (None, password),
    }
    resp = requests.post(f"{app_root_url}/api/v1/token", files=files)
    data = resp.json()
    return data.get("access_token", None)


def request_minio_galleries(token: str, page: int, size: int):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"size": size, "page": page}
    resp = requests.get(
        f"{app_root_url}/api/v1/storage/minio/storages", params=params, headers=headers
    )
    rows = resp.json()
    return [StorageMinio(**row) for row in rows]


def get_minio_galleries(token: str):
    page = 1
    size = 100
    galleries = request_minio_galleries(token, page, size)
    if len(galleries) >= size:
        page += 1
        galleries += request_minio_galleries(token, page, size)
    return galleries


pattern = "[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"


def is_uuid4(s):
    return bool(re.match(pattern, s))


def get_minio_path(gallery_path, minio_volume):
    gallery_path_relative_to_minio_volume = str(gallery_path.relative_to(minio_volume))
    if (
        len(gallery_path_relative_to_minio_volume) > 0
        and gallery_path_relative_to_minio_volume[-1] != "/"  # noqa
    ):
        gallery_path_relative_to_minio_volume += "/"
    return f"{SourceProtocolEnum.MINIO.value}-{minio_storage_id}://{gallery_path_relative_to_minio_volume}"  # noqa


def sync_new_galleries():
    if state.is_sync:
        return "sync..."
    state.is_sync = True

    # To check sync_from_path
    sync_from_path = standalone_setting.standalone_sync_galleries_from_path
    if sync_from_path is None:
        raise HTTPException(
            status_code=404, detail="'standalone_sync_galleries_from_path' not found"
        )
    sync_from_path = Path(sync_from_path)
    if not sync_from_path.exists():
        raise HTTPException(
            status_code=404, detail=f"path: {str(sync_from_path)} not found"
        )
    if not sync_from_path.is_dir():
        raise HTTPException(
            status_code=409, detail=f"path: {str(sync_from_path)} is not folder"
        )

    # To check sync_to_path
    sync_to_path = standalone_setting.standalone_sync_galleries_to_path
    if sync_to_path is None:
        raise HTTPException(
            status_code=404, detail="'standalone_sync_galleries_to_path' not found"
        )
    sync_to_path = Path(sync_to_path)
    if not sync_to_path.exists():
        raise HTTPException(
            status_code=404, detail=f"path: {str(sync_to_path)} not found"
        )
    if not sync_to_path.is_dir():
        raise HTTPException(
            status_code=409, detail=f"path: {str(sync_to_path)} is not folder"
        )

    if not elastic_client.ping():
        raise HTTPException(status_code=404, detail="Elasticsearch not found")
    minio_client.list_buckets()

    # To get token
    username = standalone_setting.app_admin_email
    password = standalone_setting.app_admin_password
    token = get_token(username, password)
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # To check if in minio galleries and minio volume
    try:
        sync_to_path_relative_to_minio_volume = sync_to_path.relative_to(minio_volume)
    except ValueError:
        raise HTTPException(
            status_code=409,
            detail=f"path: {str(sync_to_path)} should be relative to {minio_volume}",
        )
    minio_galleries = get_minio_galleries(token)
    for i in range(len(minio_galleries)):
        minio_gallery = minio_galleries[i]
        minio_galleries[i] = f"{minio_gallery.bucket_name}/{minio_gallery.prefix}"
        if len(minio_galleries[i]) > 0 and minio_galleries[i][-1] == "/":
            minio_galleries[i] = minio_galleries[i][:-1]
    if str(sync_to_path_relative_to_minio_volume) not in minio_galleries:
        raise HTTPException(
            status_code=409, detail=f"path: {str(sync_to_path)} not in minio galleries"
        )

    gallery_dir_fname = standalone_setting.gallery_dir_fname
    gallery_tag_fname = standalone_setting.gallery_tag_fname
    for gallery_path in sync_from_path.iterdir():
        if not gallery_path.is_dir():
            continue

        gallery_name = None
        new_gallery_name = gallery_name = gallery_path.name
        if not is_uuid4(gallery_path.name):
            new_gallery_name = str(uuid4())

        new_gallery_path = sync_to_path / new_gallery_name
        if new_gallery_path.exists():
            continue

        gallery_path.rename(new_gallery_path)

        # To update minio path
        # TODO: check if id is dup
        new_gallery_minio_path = get_minio_path(new_gallery_path, minio_volume)
        new_tag_path = new_gallery_path / gallery_dir_fname / gallery_tag_fname
        if new_tag_path.exists():
            with new_tag_path.open(mode="r", encoding="utf-8") as fp:
                gallery_tag = json.load(fp)
                gallery_tag = Gallery(**gallery_tag)
            gallery_tag.path = new_gallery_minio_path
        else:
            os.makedirs(new_gallery_path / gallery_dir_fname, exist_ok=True)
            now = get_now()
            gallery_tag = Gallery(
                **{
                    "id": str(uuid4()),
                    "path": new_gallery_minio_path,
                    "group": "",
                    "timestamp": now,
                    "mtime": now,
                    "attributes": {"name": gallery_name},
                }
            )
        with new_tag_path.open(mode="w", encoding="utf-8") as fp:
            json.dump(gallery_tag.dict(), fp, indent=4, ensure_ascii=False)

        # To elasticsearch
        elastic_client.index(
            index=elastic_index_gallery, id=gallery_tag.id, body=gallery_tag.dict()
        )

    state.is_sync = False


@app.get("/ping")
def get_ping(request: Request):
    print(f"From {request.client.host}")
    return 1


@app.get("/sync-new-galleries")
def get_sync_new_galleries():
    sync_new_galleries()


@app.options("/sync-new-galleries")
def options_sync_new_galleries():
    sync_new_galleries()


@app.exception_handler(HTTPException)
async def fastapi_http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=exc.status_code, content={"defail": exc.detail})


@app.exception_handler(NewConnectionError)
async def minio_new_connection_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"defail": "Minio service not known"})


@app.exception_handler(NotFoundError)
async def elastic_notfound(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"defail": "Gallery not found"})


try:
    from plugins.standalone import router as plugin

    app.include_router(plugin, prefix="/plugin")
except ModuleNotFoundError:
    pass

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
