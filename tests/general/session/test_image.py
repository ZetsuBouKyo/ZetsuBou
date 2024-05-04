from tests.general.session import ImageSession


def test_image_session():
    with ImageSession() as session:
        assert session.image_path.exists()
