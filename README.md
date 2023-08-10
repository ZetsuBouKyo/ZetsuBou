# ZetsuBou

[![Python](https://img.shields.io/badge/Python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-3811/)
[![Vue](https://img.shields.io/badge/Vue-3.3.4-yellow.svg)](https://v3.vuejs.org/)
[![chrome](https://img.shields.io/badge/Chrome-115.0.5790.99-yellow.svg)](https://www.google.com/intl/en_us/chrome/)
[![license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://www.google.com/intl/en_us/chrome/)

[ZetsuBou](https://zetsuboukyo.github.io/) is a web-based app for hosting your own image galleries and videos. The app is written in Python 3 and Vue 3.

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

### Run example

```bash
# To build the docker images
make build
# To initialize airflow and create `./etc/settings.env` and `./etc/settings.airflow.env`
make init-example
# To close the services started during initialization
make down

# To start the services
make up
```

You can find the ZetusBou webapp username (`ZETSUBOU_APP_ADMIN_EMAIL`), password (`ZETSUBOU_APP_ADMIN_PASSWORD`) and other information in `./etc/settings.env`.

## Contact

[My twitch channel](https://www.twitch.tv/zetsuboukyo)
