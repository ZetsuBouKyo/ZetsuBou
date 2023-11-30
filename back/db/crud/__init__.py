from .group.group import CrudGroup
from .scope.group import CrudScopeGroup
from .scope.scope import CrudScope
from .setting.front.gallery import CrudSettingFrontGallery
from .setting.front.video import CrudSettingFrontVideo
from .storage.minio import CrudStorageMinio
from .tag.attribute import CrudTagAttribute
from .tag.category import CrudTagCategory
from .tag.token import CrudTagToken
from .user.bookmark.gallery import CrudUserBookmarkGallery
from .user.elastic.count_query import CrudUserElasticCountQuery
from .user.elastic.search_query import CrudUserElasticSearchQuery
from .user.front_settings import CrudUserFrontSettings
from .user.group import CrudUserGroup
from .user.quest.category import CrudUserQuestCategory
from .user.quest.elastic_count_quest import CrudUserElasticCountQuest
from .user.quest.quest import CrudUserQuest
from .user.user import CrudUser

__all__ = [
    "CrudGroup",
    "CrudGroupPermission",
    "CrudScope",
    "CrudScopeGroup",
    "CrudSettingFrontGallery",
    "CrudSettingFrontVideo",
    "CrudStorageMinio",
    "CrudTagAttribute",
    "CrudTagCategory",
    "CrudTagToken",
    "CrudUser",
    "CrudUserBookmarkGallery",
    "CrudUserElasticCountQuery",
    "CrudUserElasticCountQuest",
    "CrudUserElasticSearchQuery",
    "CrudUserFrontSettings",
    "CrudUserGroup",
    "CrudUserQuest",
    "CrudUserQuestCategory",
]
