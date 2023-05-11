# ZetsuBou

[![Python](https://img.shields.io/badge/Python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-3811/)
[![Vue](https://img.shields.io/badge/Vue-3.0.11-yellow.svg)](https://v3.vuejs.org/)
[![chrome](https://img.shields.io/badge/Chrome-102.0.5005.63-yellow.svg)](https://www.google.com/intl/en_us/chrome/)
[![license](https://img.shields.io/badge/License-MIT-yellow.svg)](https://www.google.com/intl/en_us/chrome/)

ZetsuBou is a web-based app to serve your own image galleries and videos.

**There would be no backward compatibility at all.**

This is written in Python 3 and Vue 3.

## ⚠️ Warning

ZetsuBou would generate `.tag` folder inside your galleries. Here is the folder structure.

```text
+-- Gallery 001
|   +-- .tag
|   |   +-- gallery.json
|   |   +-- ...
|   +-- 1.jpg
|   +-- 2.jpg
|   +-- ...
+-- Gallery 002
|   +-- .tag
|   |   +-- gallery.json
|   |   +-- ...
|   +-- 1.png
|   +-- 2.bmp
|   +-- 3.jpg
|   +-- ...
+-- ...
```

## Development

### Set environment

```bash
# To install commitlint
npm install --save-dev @commitlint/{cli,config-conventional}
# To test commitlint
npx commitlint --from "HEAD~1" --to "HEAD" --verbose
# To install formatter
npm install --save-dev prettier prettier-eslint
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
# To up the services
make up
# To run the app
poetry run python app.py
# (Optional) To run standalone
poetry run python standalone.py
```

### Run before push

```bash
# To format the files
pre-commit run --all-files
```

## Contact

[My twitch channel](https://www.twitch.tv/demonic22)

## Reference

- [vite-vue3-tailwind-starter](https://github.com/web2033/vite-vue3-tailwind-starter)
