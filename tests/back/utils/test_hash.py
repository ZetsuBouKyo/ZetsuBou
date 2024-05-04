from back.utils.hash import get_md5
from tests.general.session import ImageSession


def test_get_md5():
    with ImageSession() as session:
        md5 = get_md5(session.image_path)
        assert md5 == "efc26bdb68f1eac2c7047b9ba5c4b0ce"
