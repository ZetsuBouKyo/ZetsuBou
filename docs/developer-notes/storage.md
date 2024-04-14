# Storage

| Name                | Where we store the information (e.g. username, password, ...) of the storages |
| ------------------- | ----------------------------------------------------------------------------- |
| ZetsuBou S3 storage | `./etc/settings.env`                                                          |
| Other S3 storages   | PostgreSQL table name: storage_minio                                          |

## ZetsuBou S3 storage

The filesystem structure in ZetsuBou S3 storage.

```text
zetsubou
├── backup
│   ├── 2023-12-30T16-31-48-479954+08-00
│   └── 2024-03-07T20-01-06-995227+08-00
│       ├── db
│       │   ├── <SQL table name>.json
│       │   ├── ...
│       │   └── <SQL table name>.json
│       └── elastic
│       │   ├── <Elasticsearch index name>.json
│       │   ├── ...
│       │   └── <Elasticsearch index name>.json
└── video
    └── cover
        └── <Video ID>.png
```

## Other S3 storages

These storages are used for storing galleries and videos.
