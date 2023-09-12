# Launch an example

## Copy the files

Clone the project from [github repository](https://github.com/ZetsuBouKyo/ZetsuBou).

```sh
git clone https://github.com/ZetsuBouKyo/ZetsuBou
```

## Build the docker images

```sh
make build
```

This command will build `zetsubou/app:0.0.1-python-3.8.16-slim-buster` and
`zetsubou/airflow:2.6.1-python3.8` docker images.

## Initialization

Create the volumes under `./dev` relative to the current working directory, and
`./etc/analysis/synonym.txt`.

```sh
make init
```

## Start the services

```sh
# To start the services
make up
```

After `make up` command, you can find the username, password, and other information in
`./etc/settings.env`. The default URL for the application is http://localhost:3000 .
