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
`zetsuboukyo/airflow-standalone:2.6.2-python3.8` docker images.

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

## Q & A

### How to Install Node.js v18.16.0+ on Ubuntu 18.04

<https://github.com/nodesource/distributions/issues/1392#issuecomment-1815887430>

```sh
sudo -i

# Start by installing Node 20:

sudo apt-get install python3 g++ make python3-pip gcc bison

curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o n
bash n 20

# Node 20 is now at /usr/local/bin/node, but glibc 2.28 is missing:
# node: /lib/aarch64-linux-gnu/libc.so.6: version `GLIBC_2.28' not found (required by node)
# /usr/local/bin/node: /lib/aarch64-linux-gnu/libc.so.6: version `GLIBC_2.28' not found (required by /usr/local/bin/node)

# Build and install glibc 2.28:
apt install -y gawk
cd ~
wget -c https://ftp.gnu.org/gnu/glibc/glibc-2.28.tar.gz
tar -zxf glibc-2.28.tar.gz
cd glibc-2.28
pwd
mkdir glibc-build
cd glibc-build
../configure --prefix=/opt/glibc-2.28
make -j 4 # Use all 4 Jetson Nano cores for much faster building
make install
cd ..
rm -fr glibc-2.28 glibc-2.28.tar.gz

# Patch the installed Node 20 to work with /opt/glibc-2.28 instead:
apt install -y patchelf
patchelf --set-interpreter /opt/glibc-2.28/lib/ld-linux-x86-64.so.2 --set-rpath /opt/glibc-2.28/lib/:/lib/x86_64-linux-gnu/:/usr/lib/x86_64-linux-gnu/ /usr/local/bin/node

# Et voilà:
node --version
v20.9.0
```

If you use `nvm` to manage `Node.js` versions, here is an example command to patch `glibc-2.28` for `Node.js` in `nvm`.

```sh
patchelf --set-interpreter /opt/glibc-2.28/lib/ld-linux-x86-64.so.2 --set-rpath /opt/glibc-2.28/lib/:/lib/x86_64-linux-gnu/:/usr/lib/x86_64-linux-gnu/ /root/.nvm/versions/node/v18.16.0/bin/node
```

Be mindful of your system architecture. If your system is not `x86-64`, you will need to adjust the `patchelf` command.
Here is an example for `aarch64`.

```sh
patchelf --set-interpreter /opt/glibc-2.28/lib/ld-linux-aarch64.so.2 --set-rpath /opt/glibc-2.28/lib/:/lib/aarch64-linux-gnu/:/usr/lib/aarch64-linux-gnu/ /usr/local/bin/node
```
