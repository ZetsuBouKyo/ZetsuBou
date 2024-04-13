# Introduction

We use [MinIO](https://github.com/minio/minio) as default storage. It is an open source
software and its API is compatible with the Amazon S3 cloud storage service.

Currently, we do not support other forms of storage, such as local storage, file
servers, etc., and have no plans to do so.

There seems to be some changes in their
[gateway](https://min.io/docs/minio/linux/operations/install-deploy-manage/migrate-fs-gateway.html).
If you don't have MinIO service or other services that support S3 API yet, the tested
version of the MinIO docker image in our application is
`zetsuboukyo/minio:RELEASE.2022-02-26T02-54-46Z.fips`.

## Add a storage

## MinIO volume structure

```text
backup
├── <date>
│   ├── db
│   │   ├── <file>.json
│   │   ├── ...
│   │   └── <file>.json
│   └── elastic
│       ├── <file>.json
│       ├── ...
│       └── <file>.json
├── <date>
│   ├── db
│   │   ├── <file>.json
│   │   ├── ...
│   │   └── <file>.json
│   └── elastic
│       ├── <file>.json
│       ├── ...
│       └── <file>.json
zetsubou
├── video
│   └── cover
│       ├── <image>.png
│       ├── ...
│       └── <image>.png
...
```
