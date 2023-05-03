-include .env
-include ./etc/settings.env
export

SHELL := /bin/bash
ZETSUBOU_TIMESTAMP ?= $(shell date +'%Y-%m-%d-%H%M')
ZETSUBOU_APP_VERSION ?= 0.0.1
ZETSUBOU_APP_MINIO ?= ./dev/minio
ZETSUBOU_APP_MINIO_GALLERIES ?= ./dev/minio/galleries
ZETSUBOU_APP_MINIO_GALLERIES_SIMPLE ?= ./dev/minio/galleries/simple
ZETSUBOU_ELASTICSEARCH_VOLUME ?= ./dev/volumes/elasticsearch
ZETSUBOU_LABEL_STUDIO_DATA_VOLUME ?= ./dev/volumes/label-studio/data
ZETSUBOU_LABEL_STUDIO_DEPLOY_VOLUME ?= ./dev/volumes/label-studio/deploy
ZETSUBOU_LABEL_STUDIO_DATA_POSTGRES_DB_VOLUME ?= ./dev/volumes/label-studio/postgres
ZETSUBOU_REDIS_VOLUME ?= ./dev/volumes/redis
ZETSUBOU_POSTGRES_DB_VOLUME ?= ./dev/volumes/postgres

AIRFLOW_UID ?= $(shell id -u)
AIRFLOW_VOLUME ?= ./dev/volumes/airflow
AIRFLOW_DAGS_VOLUME ?= ./dags
AIRFLOW_LOGS_VOLUME ?= ./dev/volumes/airflow/logs
AIRFLOW_PLUGINS_VOLUME ?= ./dev/volumes/airflow/plugins
AIRFLOW_POSTGRES_DB_VOLUME ?= ./dev/volumes/airflow/postgres

APP_DEV_SERVICES := zetsubou-postgres zetsubou-elastic zetsubou-minio
AIRFLOW_SERVICES := airflow-postgres airflow-redis airflow-webserver airflow-scheduler airflow-worker airflow-triggerer airflow-init airflow-cli flower

.PHONY: test line check

test:
	echo "$(ZETSUBOU_TIMESTAMP)"


line:
	git ls-files | xargs wc -l

EXECUTABLES = poetry docker docker-compose ffmpeg
check:
	ok := $(foreach exec,$(EXECUTABLES),\
		$(if $(shell which $(exec)), $(error "Command $(exec) not found")))

.PHONY: build build-docker-app build-docker-airflow-dev build-docker-minio-dev build-dev
build-docker-app:
	docker build --force-rm -f Dockerfile.app -t zetsubou-dev/app:${ZETSUBOU_APP_VERSION:-latest} .
build-docker-airflow-dev:
	docker build --force-rm -f Dockerfile.airflow -t zetsubou-dev/airflow:2.2.3-python3.8 .
build-dev: build-docker-airflow-dev
	poetry install
	source ./.venv/bin/activate; pre-commit install
build: build-docker-airflow-dev

.PHONY: init init-app init-app-postgres init-airflow init-app-elastic init-redis
init-app-elastic:
	mkdir -p $(ZETSUBOU_ELASTICSEARCH_VOLUME)
	chown -R 1000:1000 $(ZETSUBOU_ELASTICSEARCH_VOLUME)
init-app-postgres:
	mkdir -p $(ZETSUBOU_POSTGRES_DB_VOLUME)
init-app: init-app-elastic init-app-postgres
init-minio:
	mkdir -p $(ZETSUBOU_APP_MINIO)
	mkdir -p $(ZETSUBOU_APP_MINIO_GALLERIES)
	mkdir -p $(ZETSUBOU_APP_MINIO_GALLERIES_SIMPLE)
init-airflow:
	mkdir -p $(AIRFLOW_DAGS_VOLUME) \
		$(AIRFLOW_LOGS_VOLUME) \
		$(AIRFLOW_PLUGINS_VOLUME) \
		$(AIRFLOW_POSTGRES_DB_VOLUME)

	chown -R $(AIRFLOW_UID):$(AIRFLOW_UID) $(AIRFLOW_DAGS_VOLUME)
	chown -R $(AIRFLOW_UID):$(AIRFLOW_UID) $(AIRFLOW_LOGS_VOLUME)
	chown -R $(AIRFLOW_UID):$(AIRFLOW_UID) $(AIRFLOW_PLUGINS_VOLUME)

	docker-compose -f docker-compose.host.yml up airflow-init
init-label-studio:
	mkdir -p $(ZETSUBOU_LABEL_STUDIO_DATA_VOLUME)
	mkdir -p $(ZETSUBOU_LABEL_STUDIO_DEPLOY_VOLUME)
	mkdir -p $(ZETSUBOU_LABEL_STUDIO_DATA_POSTGRES_DB_VOLUME)
init-redis:
	mkdir -p $(ZETSUBOU_REDIS_VOLUME)
	chown -R 1001:1001 $(ZETSUBOU_REDIS_VOLUME)
init: init-app-postgres init-airflow init-app-elastic init-label-studio init-redis

.PHONY: clean clean-all clean-airflow clean-app-elastic clean-app-postgres clean-docker
clean-airflow:
	rm -rf $(AIRFLOW_VOLUME)
clean-app-elastic:
	rm -rf $(ZETSUBOU_ELASTICSEARCH_VOLUME)
clean-app-postgres:
	rm -rf $(ZETSUBOU_POSTGRES_DB_VOLUME)
clean-docker:
	docker rmi $(shell docker images -f "dangling=true" -q)
clean: clean-airflow clean-docker

clean-all:
	rm -f ./.env
	rm -rf ./dev
	rm -rf ./etc
	rm -rf ./statics
	rm -rf ./venv

.PHONY: reset-app reset-app-elastic reset-app-postgres
reset-app-elastic: clean-app-elastic init-app-elastic
reset-app-postgres: clean-app-postgres init-app-postgres
reset-app: reset-app-elastic reset-app-postgres

.PHONY: up up-airflow up-app-dev
up-airflow:
	docker-compose -f docker-compose.host.yml up -d $(AIRFLOW_SERVICES)
up-label-studio:
	docker-compose -f docker-compose.label-studio.yml up -d
up-app-dev:
	docker-compose -f docker-compose.host.yml up -d $(APP_DEV_SERVICES)
up-dev: up-airflow up-app-dev

.PHONY: start-airflow start-app-dev
start-airflow:
	docker-compose -f docker-compose.host.yml start $(AIRFLOW_SERVICES)
start-app-dev:
	docker-compose -f docker-compose.host.yml start $(APP_DEV_SERVICES)

.PHONY: stop-airflow stop-app-dev
stop-airflow:
	docker-compose -f docker-compose.host.yml stop $(AIRFLOW_SERVICES)
stop-app-dev:
	docker-compose -f docker-compose.host.yml stop $(APP_DEV_SERVICES)

.PHONY: down
down:
	docker-compose -f docker-compose.host.yml down

.PHONY: logs
logs:
	docker-compose -f docker-compose.host.yml logs $(service)

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt --without-hashes
