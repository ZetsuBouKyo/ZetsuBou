from enum import Enum


class ExampleEnum(Enum):
    USER_ID: int = 1
    USER_NAME: str = "ZetsuBouKyo"
    USER_EMAIL: str = "zetsuboukyo@example.com"
    PASSWORD: str = "password"
    NEW_PASSWORD: str = "newpassword"

    GALLERY_PREVIEW_SIZE: int = 20
    GALLERY_IMAGE_AUTO_PLAY_TIME_INTERVAL: int = 5
    GALLERY_IMAGE_PREVIEW_SIZE: int = 20
    VIDEO_PREVIEW_SIZE: int = 20
