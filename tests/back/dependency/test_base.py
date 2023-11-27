import pytest
from pydantic import ValidationError

from back.dependency.base import get_pagination


def test_get_pagination():
    page_1 = get_pagination()

    assert page_1.page == 1
    assert page_1.skip == 0
    assert page_1.is_desc is False

    with pytest.raises(ValidationError):
        get_pagination(0)

    with pytest.raises(ValidationError):
        get_pagination(-1)

    with pytest.raises(ValidationError):
        get_pagination(1, 0)

    with pytest.raises(ValidationError):
        get_pagination(1, -1)
