import asyncio
import json
import os
import re
from pathlib import Path
from shutil import which
from typing import List
from uuid import uuid4

from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException

from back.crud.async_gallery import get_gallery_by_gallery_id
from back.crud.async_progress import Progress
from back.db.crud import CrudStorageMinio
from back.db.model import StorageMinio
from back.logging import logger_zetsubou
from back.model.base import SourceProtocolEnum
from back.model.gallery import Gallery
from back.model.storage import StorageStat
from back.model.task import ZetsuBouTaskProgressEnum
from back.schema.basic import Message
from back.session.async_elasticsearch import async_elasticsearch as _async_elasticsearch
from back.session.storage.async_s3 import get_source
from back.settings import setting
from back.utils.dt import get_now
from back.utils.image import is_browser_image, is_image
from back.utils.video import is_video

ELASTIC_INDEX_GALLERY = setting.elastic_index_gallery

STANDALONE_STORAGE_PROTOCOL = setting.standalone_storage_protocol
STANDALONE_STORAGE_ID = setting.standalone_storage_id
STANDALONE_STORAGE_MINIO_VOLUME = setting.standalone_storage_minio_volume

STANDALONE_SYNC_GALLERIES_FROM_PATH = setting.standalone_sync_galleries_from_path
STANDALONE_SYNC_GALLERIES_TO_PATH = setting.standalone_sync_galleries_to_path

GALLERY_DIR_FNAME = setting.gallery_dir_fname
GALLERY_TAG_FNAME = setting.gallery_tag_fname

PATTERN = "[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"


def is_uuid4(s):
    return bool(re.match(PATTERN, s))


def _check_path(path: str) -> Path:
    if path is None:
        raise HTTPException(
            status_code=404,
            detail=f"'{path}' not found",
        )

    _path = Path(path)
    if not _path.exists():
        raise HTTPException(status_code=404, detail=f"path: {path} not found")
    if not _path.is_dir():
        raise HTTPException(
            status_code=409,
            detail=f"path: {path} is not folder",
        )
    return _path


def _check_storage_minio(
    relative_path: Path, storage_minios: List[StorageMinio]
) -> bool:
    for storage_minio in storage_minios:
        storage_minio_path = f"{storage_minio.bucket_name}/{storage_minio.prefix}"
        _storage_minio_path = Path(storage_minio_path)
        if relative_path == _storage_minio_path:
            return True
    return False


async def _check_storage_minios(relative_path: Path) -> bool:
    skip = 0
    limit = 1000
    storage_minios = await CrudStorageMinio.get_rows_order_by_id(
        skip=skip,
        limit=limit,
    )

    if _check_storage_minio(relative_path, storage_minios):
        return True

    while len(storage_minios) > 0:
        skip += limit
        storage_minios = await CrudStorageMinio.get_rows_order_by_id(
            skip=skip,
            limit=limit,
        )
        if _check_storage_minio(relative_path, storage_minios):
            return True

    return False


def _get_path_at_host(
    source_path: str, storage_volume: str = STANDALONE_STORAGE_MINIO_VOLUME
) -> Path:
    if storage_volume is None:
        raise HTTPException(
            status_code=404, detail="'STANDALONE_STORAGE_MINIO_VOLUME' not found"
        )

    relative_path = source_path.split("//")[-1]
    if len(relative_path) > 0 and relative_path[0] == "/":
        raise HTTPException(
            status_code=409,
            detail=f"Path in storage path after removing '{SourceProtocolEnum.MINIO.value}' should not start with '/'",  # noqa
        )

    path_at_host = Path(storage_volume, relative_path)
    return path_at_host


class _SyncNewGalleries:
    def __init__(
        self,
        storage_protocol: SourceProtocolEnum = None,
        storage_id: int = None,
        storage_minio_volume: str = None,
        sync_from_path: str = None,
        sync_to_path: str = None,
        gallery_dir_fname: str = None,
        gallery_tag_fname: str = None,
        elastic_index_gallery: str = None,
        async_elasticsearch: AsyncElasticsearch = None,
        is_from_setting_if_none: bool = False,
    ):
        self.storage_protocol = storage_protocol
        self.storage_id = storage_id
        self.storage_minio_volume = storage_minio_volume

        self.sync_from_path = sync_from_path
        self.sync_to_path = sync_to_path

        self.gallery_dir_fname = gallery_dir_fname
        self.gallery_tag_fname = gallery_tag_fname

        self.elastic_index_gallery = elastic_index_gallery
        self.async_elasticsearch = async_elasticsearch

        if is_from_setting_if_none:
            if self.storage_protocol is None:
                self.storage_protocol = STANDALONE_STORAGE_PROTOCOL
            if self.storage_id is None:
                self.storage_id = STANDALONE_STORAGE_ID
            if self.storage_minio_volume is None:
                self.storage_minio_volume = STANDALONE_STORAGE_MINIO_VOLUME
            if self.sync_from_path is None:
                self.sync_from_path = STANDALONE_SYNC_GALLERIES_FROM_PATH
            if self.sync_to_path is None:
                self.sync_to_path = STANDALONE_SYNC_GALLERIES_TO_PATH
            if self.gallery_dir_fname is None:
                self.gallery_dir_fname = GALLERY_DIR_FNAME
            if self.gallery_tag_fname is None:
                self.gallery_tag_fname = GALLERY_TAG_FNAME
            if self.elastic_index_gallery is None:
                self.elastic_index_gallery = ELASTIC_INDEX_GALLERY
            if self.async_elasticsearch is None:
                self.async_elasticsearch = _async_elasticsearch

        self._sync_from_path = _check_path(self.sync_from_path)
        self._sync_to_path = _check_path(self.sync_to_path)

    def _get_storage_path(self, gallery_path: Path, storage_volume_path: Path):
        # Gallery path relative to storage volume
        relative_path = str(gallery_path.relative_to(storage_volume_path))

        if len(relative_path) > 0 and relative_path[-1] != "/":
            relative_path += "/"
        return f"{self.storage_protocol}-{self.storage_id}://{relative_path}"

    async def _sync_new_minio_storage(self):
        self._minio_volume_path = _check_path(self.storage_minio_volume)
        try:
            relative_path = self._sync_to_path.relative_to(self._minio_volume_path)
        except ValueError:
            raise HTTPException(
                status_code=409,
                detail=f"path: {self._sync_to_path} should be relative to {self._minio_volume_path}",  # noqa
            )

        if not await _check_storage_minios(relative_path):
            raise HTTPException(
                status_code=409,
                detail=f"path: {self._sync_to_path} not in minio galleries",
            )

        progress_id = ZetsuBouTaskProgressEnum.SYNC_NEW_GALLERIES.value
        gallery_paths = [
            gallery_path for gallery_path in self._sync_from_path.iterdir()
        ]
        async for gallery_path in Progress(
            gallery_paths, id=progress_id, is_from_setting_if_none=True
        ):
            if not gallery_path.is_dir():
                continue

            images = [
                image for image in gallery_path.glob("*") if is_browser_image(image)
            ]
            pages = len(images)

            gallery_name = None
            new_gallery_name = gallery_name = gallery_path.name
            if not is_uuid4(gallery_path.name):
                new_gallery_name = str(uuid4())

            new_gallery_path = self._sync_to_path / new_gallery_name
            if new_gallery_path.exists():
                continue

            gallery_path.rename(new_gallery_path)

            # TODO: check if id is dup
            new_gallery_minio_path = self._get_storage_path(
                new_gallery_path, self._minio_volume_path
            )
            new_tag_path = (
                new_gallery_path / self.gallery_dir_fname / self.gallery_tag_fname
            )
            if new_tag_path.exists():
                with new_tag_path.open(mode="r", encoding="utf-8") as fp:
                    gallery_tag = json.load(fp)
                    gallery_tag = Gallery(**gallery_tag)
                gallery_tag.path = new_gallery_minio_path
                gallery_tag.attributes.pages = pages
            else:
                os.makedirs(new_gallery_path / self.gallery_dir_fname, exist_ok=True)
                now = get_now()
                gallery_tag = Gallery(
                    **{
                        "id": str(uuid4()),
                        "path": new_gallery_minio_path,
                        "name": gallery_name,
                        "last_updated": now,
                        "upload_date": now,
                        "attributes": {"pages": pages},
                    }
                )
            with new_tag_path.open(mode="w", encoding="utf-8") as fp:
                json.dump(gallery_tag.dict(), fp, indent=4, ensure_ascii=False)

            # To elasticsearch
            await self.async_elasticsearch.index(
                index=self.elastic_index_gallery,
                id=gallery_tag.id,
                body=gallery_tag.dict(),
            )

    async def _sync_new_storage(self):
        if self.storage_protocol == SourceProtocolEnum.MINIO:
            storage = await CrudStorageMinio.get_row_by_id(self.storage_id)
            if storage is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"{self.storage_protocol}: {self.storage_id} not found",
                )
            await self._sync_new_minio_storage()

    async def sync(self):
        if not await self.async_elasticsearch.ping():
            raise HTTPException(status_code=404, detail="Elasticsearch not found")

        await self._sync_new_storage()


async def sync_new_galleries():
    sync_new = _SyncNewGalleries(is_from_setting_if_none=True)
    await sync_new.sync()


async def open_folder(gallery_id: str):
    gallery = await get_gallery_by_gallery_id(gallery_id)
    path_at_host = _get_path_at_host(gallery.path)
    logger_zetsubou.info(path_at_host)

    preferred_app = "nautilus"
    if which(preferred_app) is not None:
        cmd = f'{preferred_app} "{str(path_at_host)}"'
        await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        return Message(detail="ok")
    return Message(detail=f"{preferred_app}: command not found")


async def get_storage_stat(
    protocol: SourceProtocolEnum, storage_id: int
) -> StorageStat:
    if protocol == SourceProtocolEnum.MINIO.value:
        storage = await CrudStorageMinio.get_row_by_id(storage_id)
        source = get_source(storage.bucket_name, storage.prefix)
        source_path = source.path
        storage_path_at_host = _get_path_at_host(source_path)

        image_depth = storage.depth + 1

        stat = StorageStat()
        for f in storage_path_at_host.glob("**/*"):
            relative_f = f.relative_to(storage_path_at_host)
            relative_f_str = str(relative_f)
            relative_f_depth = len(relative_f_str.split("/"))

            if not f.is_file():
                if relative_f_depth == storage.depth:
                    stat.num_galleries += 1
                continue

            stat.num_files += 1
            stat.size += f.stat().st_size

            if relative_f_depth == image_depth and is_image(f):
                stat.num_images += 1

            if storage.depth == -1 and is_video(f):
                stat.num_mp4s += 1

        return stat
