from back.model.group import BuiltInGroupEnum
from back.model.scope import ScopeEnum

guest_scopes = [
    ScopeEnum.elasticsearch_query_examples_get,
    ScopeEnum.elasticsearch_analyzers_get,
    ScopeEnum.gallery_images_get,
    ScopeEnum.gallery_image_get,
    ScopeEnum.gallery_cover_get,
    ScopeEnum.gallery_random_get,
    ScopeEnum.gallery_advanced_search_get,
    ScopeEnum.gallery_search_get,
    ScopeEnum.gallery_tag_get,
    ScopeEnum.setting_front_general_get,
    ScopeEnum.setting_user_quest_categories_get,
    ScopeEnum.setting_user_quest_category_get,
    ScopeEnum.user_total_bookmarks_get,
    ScopeEnum.user_bookmarks_gallery_get,
    ScopeEnum.user_bookmarks_gallery_detail_get,
    ScopeEnum.user_bookmark_gallery_get,
    ScopeEnum.user_bookmark_gallery_post,
    ScopeEnum.user_bookmark_gallery_put,
    ScopeEnum.user_bookmark_gallery_delete,
    ScopeEnum.user_front_settings_get,
    ScopeEnum.user_front_settings_put,
    ScopeEnum.user_elastic_total_count_queries_get,
    ScopeEnum.user_elastic_count_queries_get,
    ScopeEnum.user_elastic_count_query_get,
    ScopeEnum.user_elastic_count_query_post,
    ScopeEnum.user_elastic_count_query_put,
    ScopeEnum.user_elastic_count_query_delete,
    ScopeEnum.user_elastic_total_search_queries_get,
    ScopeEnum.user_elastic_search_queries_get,
    ScopeEnum.user_elastic_search_query_get,
    ScopeEnum.user_elastic_search_query_post,
    ScopeEnum.user_elastic_search_query_put,
    ScopeEnum.user_elastic_search_query_delete,
    ScopeEnum.user_total_elastic_count_quests_get,
    ScopeEnum.user_elastic_count_quests_get,
    ScopeEnum.user_elastic_count_quest_get,
    ScopeEnum.user_elastic_count_quest_post,
    ScopeEnum.user_elastic_count_quest_put,
    ScopeEnum.user_elastic_count_quest_delete,
    ScopeEnum.user_current_quest_progress_get,
    ScopeEnum.user_total_quests_get,
    ScopeEnum.user_quests_get,
    ScopeEnum.user_quest_post,
    ScopeEnum.user_quest_put,
    ScopeEnum.user_quest_delete,
    ScopeEnum.video_get,
    ScopeEnum.video_cover_get,
    ScopeEnum.video_random_get,
    ScopeEnum.video_advanced_search_get,
    ScopeEnum.video_search_get,
    ScopeEnum.video_tag_get,
]

builtin_groups = {
    BuiltInGroupEnum.admin.value: [scope.value for scope in ScopeEnum],
    BuiltInGroupEnum.guest.value: [scope.value for scope in guest_scopes],
}