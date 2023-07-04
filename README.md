# ZetsuBou

[![Python](https://img.shields.io/badge/Python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-3811/)
[![Vue](https://img.shields.io/badge/Vue-3.0.11-yellow.svg)](https://v3.vuejs.org/)
[![chrome](https://img.shields.io/badge/Chrome-102.0.5005.63-yellow.svg)](https://www.google.com/intl/en_us/chrome/)
[![license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://www.google.com/intl/en_us/chrome/)

ZetsuBou is a web-based app for hosting your own image galleries and videos. The app is written in Python 3 and Vue 3.

**There would be no backwards compatibility at all.**

## ⚠️ Warning

ZetsuBou would generate a `.tag` folder inside your galleries. Here is an example of the folder structure.

```text
<your image galleries>
├── <your image gallery 001>
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.jpg
│   ├── 4.jpg
│   ├── 5.jpg
│   └── .tag
│       └── gallery.json
└── <your image gallery 002>
    ├── 1.jpg
    ├── 2.jpg
    ├── 3.jpg
    ├── 4.jpg
    └── .tag
        └── gallery.json
```

## Getting started

```bash
# To build docker image
make build
# To initialize airflow and create `./etc/settings.env` and `./etc/settings.airflow.env`
make init
# To close the services started during initialization
make down

# To start the services
make up
```

## Development

### Architecture

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
    Network <|-- ZetsuBou
    Network <|-- MinIO
```

### Set environment

```bash
# To install commitlint
npm install --save-dev @commitlint/{cli,config-conventional} conventional-changelog prettier prettier-eslint
# To test commitlint
npx commitlint --from "HEAD~1" --to "HEAD" --verbose
```

### Build

```bash
# To build docker images and so on
make build
# To install python packages
poetry install
# To inject pre-commit into git
pre-commit install
```

### Run

```bash
# To initialize the folders and airflow
make init
# To run the services
make up-dev
# To run the app
poetry run python app.py
# (Optional) To run standalone
poetry run python standalone.py
```

### Run before push

```bash
# To format the files
make lint
```

## Contact

[My twitch channel](https://www.twitch.tv/demonic22)
