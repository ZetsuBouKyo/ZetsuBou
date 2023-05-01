from back.model.base import Pagination


def get_pagination(page: int = 1, size: int = 20, is_desc: bool = False) -> Pagination:
    return Pagination(page=page, size=size, is_desc=is_desc)
