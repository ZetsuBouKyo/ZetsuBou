from back.db.crud.group.group import CrudGroup
from back.db.crud.scope.group import CrudScopeGroup
from back.db.crud.scope.scope import CrudScope
from back.db.crud.setting.front.gallery import CrudSettingFrontGallery
from back.db.crud.setting.front.video import CrudSettingFrontVideo
from back.db.crud.storage.minio import CrudStorageMinio
from back.db.crud.tag.attribute import CrudTagAttribute
from back.db.crud.tag.category import CrudTagCategory
from back.db.crud.tag.token import CrudTagToken
from back.db.crud.user.bookmark.gallery import CrudUserBookmarkGallery
from back.db.crud.user.elastic.count_query import CrudUserElasticCountQuery
from back.db.crud.user.elastic.search_query import CrudUserElasticSearchQuery
from back.db.crud.user.front_settings import CrudUserFrontSettings
from back.db.crud.user.group import CrudUserGroup
from back.db.crud.user.quest.category import CrudUserQuestCategory
from back.db.crud.user.quest.elastic_count_quest import CrudUserElasticCountQuest
from back.db.crud.user.quest.quest import CrudUserQuest
from back.db.crud.user.user import CrudUser

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
