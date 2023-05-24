from enum import Enum, auto

from pydantic import BaseModel


class ScopeEnum(int, Enum):
    admin: int = auto()
    guest: int = auto()

    elasticsearch: int = auto()
    elasticsearch_query_examples_get: int = auto()
    elasticsearch_analyzers_get: int = auto()

    gallery: int = auto()
    gallery_images_get: int = auto()
    gallery_image_get: int = auto()
    gallery_cover_get: int = auto()
    gallery_delete: int = auto()
    gallery_open_get: int = auto()
    gallery_query: int = auto()
    gallery_query_count_field_value_get: int = auto()
    gallery_query_count_post: int = auto()
    gallery_query_random_get: int = auto()
    gallery_query_custom_search_post: int = auto()
    gallery_query_advanced_search_get: int = auto()
    gallery_query_search_get: int = auto()
    gallery_tag: int = auto()
    gallery_tag_get: int = auto()
    gallery_tag_post: int = auto()

    storage_minio: int = auto()
    storage_minio_operation_list_get: int = auto()
    storage_minio_operation_stat_get: int = auto()
    storage_minio_storage: int = auto()
    storage_minio_storages_get: int = auto()
    storage_minio_storage_post: int = auto()
    storage_minio_storage_put: int = auto()
    storage_minio_storage_delete: int = auto()
    storage_minio_storage_categories_get: int = auto()
    storage_minio_total_storages_get: int = auto()

    setting: int = auto()
    setting_front: int = auto()
    setting_front_general_get: int = auto()
    setting_front_gallery: int = auto()
    setting_front_gallery_category_startswith_get: int = auto()
    setting_front_gallery_tag_field_startswith_get: int = auto()
    setting_front_gallery_interpretation_get: int = auto()
    setting_front_gallery_reset_get: int = auto()
    setting_front_gallery_get: int = auto()
    setting_front_gallery_put: int = auto()
    setting_front_video: int = auto()
    setting_front_video_category_startswith_get: int = auto()
    setting_front_video_tag_field_startswith_get: int = auto()
    setting_front_video_interpretation_get: int = auto()
    setting_front_video_reset_get: int = auto()
    setting_front_video_get: int = auto()
    setting_front_video_put: int = auto()

    tag: int = auto()
    tag_search_for_tag_attributes_get: int = auto()
    tag_interpretation_get: int = auto()
    tag_get: int = auto()
    tag_delete: int = auto()
    tag_post: int = auto()
    tag_put: int = auto()

    tag_attribute: int = auto()
    tag_total_attributes_get: int = auto()
    tag_attributes_get: int = auto()
    tag_attribute_post: int = auto()
    tag_attribute_put: int = auto()
    tag_attribute_delete: int = auto()

    tag_category: int = auto()
    tag_categories_get: int = auto()
    tag_category_post: int = auto()
    tag_category_delete: int = auto()

    tag_synonym: int = auto()
    tag_synonyms_get: int = auto()
    tag_synonym_post: int = auto()
    tag_synonym_put: int = auto()
    tag_synonym_delete: int = auto()

    tag_token: int = auto()
    tag_token_startswith_get: int = auto()
    tag_toal_tokens_get: int = auto()
    tag_token_exists_get: int = auto()
    tag_token_get: int = auto()
    tag_tokens_get: int = auto()
    tag_token_post: int = auto()
    tag_token_put: int = auto()
    tag_token_delete: int = auto()

    task: int = auto()
    task_cmd: int = auto()
    task_standalone_gallery_open_get: int = auto()
    task_standalone_gallery_sync_new_galleries_get: int = auto()
    task_standalone_gallery_ping_get: int = auto()

    user: int = auto()
    user_post: int = auto()
    user_get: int = auto()
    user_put: int = auto()
    user_delete: int = auto()
    user_groups_get: int = auto()
    user_groups_post: int = auto()
    user_front_setting_get: int = auto()
    user_front_setting_put: int = auto()
    user_elastic_total_count_queries_get: int = auto()
    user_elastic_count_queries_get: int = auto()
    user_elastic_count_query_get: int = auto()
    user_elastic_count_query_post: int = auto()
    user_elastic_count_query_put: int = auto()
    user_elastic_count_query_delete: int = auto()
    user_elastic_total_search_queries_get: int = auto()
    user_elastic_search_queries_get: int = auto()
    user_elastic_search_query_get: int = auto()
    user_elastic_search_query_post: int = auto()
    user_elastic_search_query_put: int = auto()
    user_elastic_search_query_delete: int = auto()
    user_quest_categories_get: int = auto()
    user_quest_category_get: int = auto()
    user_total_elastic_count_quests_get: int = auto()
    user_elastic_count_quest_get: int = auto()
    user_elastic_count_quests_get: int = auto()
    user_elastic_count_quest_post: int = auto()
    user_elastic_count_quest_put: int = auto()
    user_elastic_count_quest_delete: int = auto()
    user_current_quest_progress_get: int = auto()
    user_total_quests_get: int = auto()
    user_quests_get: int = auto()
    user_quest_post: int = auto()
    user_quest_put: int = auto()
    user_quest_delete: int = auto()

    video: int = auto()
    video_get: int = auto()
    video_cover_get: int = auto()
    video_cover_set: int = auto()
    video_query_random_get: int = auto()
    video_query_advanced_search_get: int = auto()
    video_query_search_get: int = auto()
    video_tag_get: int = auto()
    video_tag_post: int = auto()

    group: int = auto()
    total_groups_get: int = auto()
    groups_get: int = auto()
    group_post: int = auto()
    group_put: int = auto()
    group_get: int = auto()
    group_delete: int = auto()

    sys: int = auto()
    sys_setting_get: int = auto()
    sys_basic_setting_get: int = auto()

    users_get: int = auto()


class Scope(BaseModel):
    id: ScopeEnum
    group_id: int


ScopeCreate = ScopeUpdate = Scope
