from typing import List

from back.model.base import SourceBaseModel


class CrudAsyncStorageBase:
    def get_joined_source(
        self, base_source: SourceBaseModel, relative_path: str
    ) -> SourceBaseModel:
        _base_path = base_source.path
        _relative_path = relative_path
        if not _base_path.endswith("/"):
            _base_path += "/"
        if _relative_path.startswith("/"):
            _relative_path = _relative_path[1:]
        return SourceBaseModel(path=_base_path + "/" + _relative_path)

    async def get_url(self, source: SourceBaseModel) -> str:
        raise NotImplementedError

    async def get_object(self, source: SourceBaseModel) -> bytes:
        raise NotImplementedError

    async def list_filenames(self, source: SourceBaseModel) -> List[str]:
        raise NotImplementedError

    async def exists(self, source: SourceBaseModel) -> bool:
        raise NotImplementedError

    async def put_object(
        self, source: SourceBaseModel, body: bytes, content_type: str = None
    ):
        raise NotImplementedError

    async def put_json(
        self,
        source: SourceBaseModel,
        data: dict,
        indent=4,
        ensure_ascii=False,
        encoding: str = "utf-8",
    ):
        raise NotImplementedError

    async def delete(self, source: SourceBaseModel) -> bool:
        raise NotImplementedError
