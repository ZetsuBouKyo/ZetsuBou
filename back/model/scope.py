from enum import Enum


class ScopeEnum(str, Enum):
    admin: str = "admin"
    guest: str = "guest"

    elasticsearch: str = ""
    elasticsearch_query_examples_get: str = "elasticsearch.query-examples:get"
    elasticsearch_analyzers_get: str = "elasticsearch.analyzers:get"

    gallery: str = "gallery"
    gallery_images_get: str = "gallery.images:get"
    gallery_image_get: str = "gallery.image:get"
    gallery_cover_get: str = "gallery.cover:get"
    gallery_delete: str = "gallery:delete"
    gallery_open_get: str = "gallery.open:get"
    gallery_count_field_value_get: str = "gallery.count.field.value:get"
    gallery_count_post: str = "gallery.count:post"
    gallery_random_get: str = "gallery.random:get"
    gallery_custom_search_post: str = "gallery.custom-search:post"
    gallery_advanced_search_get: str = "gallery.advanced-search:get"
    gallery_search_get: str = "gallery.search:get"
    gallery_tag_get: str = "gallery.tag:get"
    gallery_tag_post: str = "gallery.tag:post"

    storage_minio: str = "storage.minio"
    storage_minio_list_get: str = "storage.minio.list:get"
    storage_minio_storages_get: str = "storage.minio.storages:get"
    storage_minio_storage_post: str = "storage.minio.storage:post"
    storage_minio_storage_put: str = "storage.minio.storage:put"
    storage_minio_storage_delete: str = "storage.minio.storage:delete"
    storage_minio_storage_categories_get: str = "storage.minio.storage-categories:get"
    storage_minio_total_storages_get: str = "storage.minio.total-storages:get"

    setting: str = "setting"
    setting_front_general_get: str = "setting.front.general:get"
    setting_front_gallery_category_startswith_get: str = (
        "setting.front.gallery.category-startswith:get"
    )
    setting_front_gallery_tag_field_startswith_get: str = (
        "setting.front.gallery.tag-field-startswith:get"
    )
    setting_front_gallery_interpretation_get: str = (
        "setting.front.gallery.interpretation:get"
    )
    setting_front_gallery_reset_get: str = "setting.front.gallery.reset:get"
    setting_front_gallery_get: str = "setting.front.gallery:get"
    setting_front_gallery_put: str = "setting.front.gallery:put"
    setting_front_video_category_startswith_get: str = (
        "setting.front.video.category-startswith:get"
    )
    setting_front_video_tag_field_startswith_get: str = (
        "setting.front.video.tag-field-startswith:get"
    )
    setting_front_video_interpretation_get: str = (
        "setting.front.video.interpretation:get"
    )
    setting_front_video_reset_get: str = "setting.front.video.reset:get"
    setting_front_video_get: str = "setting.front.video:get"
    setting_front_video_put: str = "setting.front.video:put"
    setting_user_quest_categories_get: str = "setting:user-quest-categories:get"
    setting_user_quest_category_get: str = "setting:user-quest-category:get"

    tag: str = "tag"
    tag_search_for_tag_attributes_get: str = "tag.search-for-tag-attributes:get"
    tag_interpretation_get: str = "tag.interpretation:get"
    tag_get: str = "tag:get"
    tag_delete: str = "tag:delete"
    tag_post: str = "tag:post"
    tag_put: str = "tag:put"

    tag_total_attributes_get: str = "tag.total-attributes:get"
    tag_attributes_get: str = "tag.attributes:get"
    tag_attribute_post: str = "tag.attribute:post"
    tag_attribute_put: str = "tag.attribute:put"
    tag_attribute_delete: str = "tag.attribute:delete"

    tag_categories_get: str = "tag.categories:get"
    tag_category_post: str = "tag.category:post"
    tag_category_delete: str = "tag.category:delete"

    tag_synonyms_get: str = "tag.synonyms:get"
    tag_synonym_post: str = "tag.synonym:post"
    tag_synonym_put: str = "tag.synonym:put"
    tag_synonym_delete: str = "tag.synonym:delete"

    tag_token_startswith_get: str = "tag.token-startswith:get"
    tag_toal_tokens_get: str = "tag.toal-tokens:get"
    tag_token_exists_get: str = "tag.token.exists:get"
    tag_token_get: str = "tag.token:get"
    tag_tokens_get: str = "tag.tokens:get"
    tag_token_post: str = "tag.token:post"
    tag_token_put: str = "tag.token:put"
    tag_token_delete: str = "tag.token:delete"

    task_cmd: str = "task-cmd"
    task_standalone_gallery_open_get: str = "task.standalone.gallery.open:get"
    task_standalone_gallery_sync_new_galleries_get: str = (
        "task.standalone.gallery.sync-new-galleries:get"
    )
    task_standalone_ping_get: str = "task.standalone.ping:get"

    users_get: str = "users:get"
    user_post: str = "user:post"
    user_get: str = "user:get"
    user_put: str = "user:put"
    user_delete: str = "user:delete"
    user_groups_get: str = "user.groups:get"
    user_groups_post: str = "user.groups:post"
    user_front_setting_get: str = "user.front-setting:get"
    user_front_setting_put: str = "user.front-setting:put"
    user_elastic_total_count_queries_get: str = "user.elastic.total-count-queries:get"
    user_elastic_count_queries_get: str = "user.elastic.count-queries:get"
    user_elastic_count_query_get: str = "user.elastic.count-query:get"
    user_elastic_count_query_post: str = "user.elastic.count-query:post"
    user_elastic_count_query_put: str = "user.elastic.count-query:put"
    user_elastic_count_query_delete: str = "user.elastic.count-query:delete"
    user_elastic_total_search_queries_get: str = "user.elastic.total-search-queries:get"
    user_elastic_search_queries_get: str = "user.elastic.search-queries:get"
    user_elastic_search_query_get: str = "user.elastic.search-query:get"
    user_elastic_search_query_post: str = "user.elastic.search-query:post"
    user_elastic_search_query_put: str = "user.elastic.search-query:put"
    user_elastic_search_query_delete: str = "user.elastic.search-query:delete"
    user_total_elastic_count_quests_get: str = "user.total-elastic-count-quests:get"
    user_elastic_count_quests_get: str = "user.elastic-count-quests:get"
    user_elastic_count_quest_get: str = "user.elastic-count-quest:get"
    user_elastic_count_quest_post: str = "user.elastic-count-quest:post"
    user_elastic_count_quest_put: str = "user.elastic-count-quest:put"
    user_elastic_count_quest_delete: str = "user.elastic-count-quest:delete"
    user_current_quest_progress_get: str = "user.current-quest-progress:get"
    user_total_quests_get: str = "user.total-quests:get"
    user_quests_get: str = "user.quests:get"
    user_quest_post: str = "user.quest:post"
    user_quest_put: str = "user.quest:put"
    user_quest_delete: str = "user.quest:delete"

    video: str = "video"
    video_get: str = "video:get"
    video_cover_get: str = "video.cover:get"
    video_random_get: str = "video.random:get"
    video_advanced_search_get: str = "video.advanced-search:get"
    video_search_get: str = "video.search:get"
    video_tag_get: str = "video.tag:get"
    video_tag_post: str = "video.tag:post"

    group: str = "group"
    total_groups_get: str = "total-groups:get"
    groups_get: str = "groups:get"
    group_post: str = "group:post"
    group_put: str = "group:put"
    group_get: str = "group:get"
    group_delete: str = "group:delete"

    sys_setting_get: str = ""
    sys_basic_setting_get: str = ""