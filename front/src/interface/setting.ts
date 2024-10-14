export enum AppModeEnum {
    Standalone = "standalone",
    Cluster = "cluster",
}

export enum DatabaseTypeEnum {
    Sqlite = "sqlite",
    Postgresql = "postgresql",
}

export enum LoggingLevelEnum {
    Critical = "CRITICAL",
    Fatal = "FATAL",
    Error = "ERROR",
    Warning = "WARNING",
    Warn = "WARN",
    Info = "INFO",
    Debug = "DEBUG",
    Notset = "NOTSET",
}

export enum SourceProtocolEnum {
    Minio = "minio",
}

export interface Setting {
    app_host?: string;
    app_security?: boolean;
    app_port?: number;
    app_mode?: AppModeEnum;
    app_timezone?: string;
    app_docs?: boolean;
    app_redoc?: boolean;
    app_title?: string;
    app_front?: string;
    app_front_docs?: string;
    app_favicon?: string;
    app_statics?: string;
    app_docs_swagger_js_url?: string;
    app_docs_swagger_css_url?: string;
    app_docs_redoc_js_url?: string;
    app_user_front_settings_gallery_image_auto_play_time_interval?: number;
    app_user_front_settings_gallery_image_preview_size?: number;
    app_user_front_settings_gallery_preview_size?: number;
    app_user_front_settings_video_preview_size?: number;
    app_admin_name?: string;
    app_admin_email?: string;
    app_admin_password?: string;
    app_security_algorithm?: string;
    app_security_expired?: number;
    app_security_secret?: string;
    app_logging_to_file?: boolean;
    app_logging_level?: LoggingLevelEnum;
    app_logging_formatter_fmt?: string;
    app_gallery_sync_pages?: boolean;
    app_gallery_sync_pages_when_go_to_gallery?: boolean;
    standalone_storage_protocol?: SourceProtocolEnum;
    standalone_storage_id?: number;
    standalone_storage_minio_volume?: string;
    standalone_sync_galleries_from_path?: string;
    standalone_sync_galleries_to_path?: string;
    gallery_dir_fname?: string;
    gallery_backup_count?: number;
    gallery_tag_fname?: string;
    gallery_imgs_fname?: string;
    database_type?: DatabaseTypeEnum;
    database_url?: string;
    database_echo?: boolean;
    database_port?: number;
    elastic_urls?: string;
    elastic_size?: number;
    elastic_index_gallery?: string;
    elastic_index_video?: string;
    elastic_index_tag?: string;
    elasticsearch_port?: number;
    storage_protocol?: SourceProtocolEnum;
    storage_expires_in_minutes?: number;
    storage_cache?: string;
    storage_backup?: string;
    storage_s3_aws_access_key_id?: string;
    storage_s3_aws_secret_access_key?: string;
    storage_s3_endpoint_url?: string;
    storage_s3_volume?: string;
    storage_s3_port?: number;
    storage_s3_console_port?: number;
    airflow_host?: string;
    airflow_username?: string;
    airflow_password?: string;
    airflow_create_admin?: boolean;
    airflow_web_server_port?: number;
    airflow_standalone_volume?: string;
    airflow_download_volume?: string;
    redis_url?: string;
    redis_port?: number;
}
