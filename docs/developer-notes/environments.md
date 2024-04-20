# Environments

## Set up an environment

### NPM

We use [commitlint](https://github.com/conventional-changelog/commitlint) and
[prettier](https://github.com/prettier/prettier) to format the codes.

```sh
# To install commitlint, prettier and so on
npm install --also=dev
# To test commitlint
npx commitlint --from "HEAD~1" --to "HEAD" --verbose
```

### Python

We use [poetry](https://github.com/python-poetry/poetry) to organize the Python packages
.

```sh
poetry install
```

The [pre-commit](https://github.com/pre-commit/pre-commit) is used to hook the
formatters and validators.

```sh
pre-commit install
```

### Rust

Rust is used to tune the performance. We use [pyo3](https://github.com/PyO3/pyo3) as the
bindings between Python and Rust.

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Build

### Build the docker images

```sh
make build
```

This command will build `zetsuboukyo/app:0.0.1-python-3.8.16-slim-buster` and
`zetsuboukyo/airflow-simple:2.6.2-python3.8` docker images.

### Build frontend

```sh
cd front
npm install --also=dev
npm run build
cd ..
```

### Build documentation

Create the static docs files in `./front/doc_site`.

```sh
make docs
```

## Run

Create the volumes under `./dev` relative to the current working directory, and
`./etc/analysis/synonym.txt`.

```sh
make init
```

Start the services with Docker containers except the ZetsuBou web application.

```sh
make up-dev
```

Run the ZetsuBou web application in Python CLI.

=== "Python"

    ``` sh
    python cli.py run
    ```

=== "With Poetry"

    ``` sh
    poetry run python cli.py run
    ```

Or you can run `app.py` directly if you need to.

=== "Python"

    ``` sh
    python app.py
    ```

=== "With Poetry"

    ``` sh
    poetry run python app.py
    ```

### Run before you push the codes

You should run the following command for every commit or you can run the commands
manually.

=== "Makefile"

    ``` sh
    make lint
    ```

=== "Manually"

    ``` sh
    # To format the files
    pre-commit run --all-files
    # To check the commit format. This command checks only one commit. If you want to
    # check multiple commits, you can change the number in `HEAD~1`.
    npx commitlint --from "HEAD~1" --to "HEAD" --verbose
    ```

## Recommended VScode extensions

| Extensions                                                                                                 | Description                               |
| ---------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| [bradlc.vscode-tailwindcss](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss) | For Tailwindcss autocomplete.             |
| [ms-python.isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)                     | To automatically sort the Python import.  |
| [redhat.vscode-yaml](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)               | For yaml autocomplete, e.g. `mkdocs.yml`. |
