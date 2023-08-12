# Architecture

```mermaid
---
title: ZetsuBou architecture
---
classDiagram
    class Network {
        port: 3000 (ZetsuBou)
        port: 9000 (MinIO)
    }
    class ZetsuBou{
        port: 3000
    }
    class Airflow{
        port: 8080
    }
    class Elasticsearch{
        port: 9200
    }
    class MinIO{
        port: 9000
        port: 9001
    }
    class PostgreSQL{
        port: 5430
    }
    class Redis{
        port: 6380
    }
    ZetsuBou <|-- Airflow
    ZetsuBou <|-- Elasticsearch
    ZetsuBou <|-- MinIO
    ZetsuBou <|-- PostgreSQL
    ZetsuBou <|-- Redis
    Airflow <|-- Elasticsearch
    Airflow <|-- MinIO
    Airflow <|-- PostgreSQL
    Airflow <|-- Redis
    Network <|-- ZetsuBou
    Network <|-- MinIO
```

| Services      | Description                                                                |
| ------------- | -------------------------------------------------------------------------- |
| Airflow       | Manage the tasks, e.g. synchronization, creating a video cover, and so on. |
| Elasticsearch | Search engine.                                                             |
| MinIO         | An object storage for hosting images, videos, and files.                   |
| PostgreSQL    | An object-relational database.                                             |
| Redis         | Maintain the status of tasks.                                              |
