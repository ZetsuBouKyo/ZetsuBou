-include ./etc/settings.env
export

SHELL := /bin/bash
ZETSUBOU_TIMESTAMP ?= $(shell date +'%Y-%m-%d-%H%M')
ZETSUBOU_APP_VERSION ?= 0.0.1
ZETSUBOU_APP_MINIO ?= ./dev/minio
ZETSUBOU_APP_MINIO_GALLERIES ?= ./dev/minio/galleries
ZETSUBOU_APP_MINIO_GALLERIES_SIMPLE ?= ./dev/minio/galleries/simple
ZETSUBOU_ELASTICSEARCH_VOLUME ?= ./dev/volumes/elasticsearch
ZETSUBOU_REDIS_VOLUME ?= ./dev/volumes/redis
ZETSUBOU_POSTGRES_DB_VOLUME ?= ./dev/volumes/postgres

AIRFLOW_UID ?= $(shell id -u)
AIRFLOW_VOLUME ?= ./dev/volumes/airflow
AIRFLOW_DAGS_VOLUME ?= ./dags
AIRFLOW_LOGS_VOLUME ?= ./dev/volumes/airflow/logs
AIRFLOW_PLUGINS_VOLUME ?= ./dev/volumes/airflow/plugins
AIRFLOW_POSTGRES_DB_VOLUME ?= ./dev/volumes/airflow/postgres

AIRFLOW_SIMPLE_VOLUME ?= ./dev/volumes/airflow-simple

APP_SERVICES := zetsubou-app zetsubou-airflow zetsubou-elastic zetsubou-minio zetsubou-postgres zetsubou-redis
APP_DEV_SERVICES := zetsubou-airflow zetsubou-elastic zetsubou-minio zetsubou-postgres zetsubou-redis

.PHONY: test line check

test:
	echo "$(ZETSUBOU_TIMESTAMP)"


line:
	git ls-files | xargs wc -l || true

check:
	@docker > /dev/null 2>&1
	@docker-compose > /dev/null 2>&1
check-dev:
	@poetry > /dev/null 2>&1
	@docker > /dev/null 2>&1
	@docker-compose > /dev/null 2>&1
	@npm --version > /dev/null 2>&1

.PHONY: build build-docker-app build-docker-airflow build-docker-minio-dev build-dev
build-docker-app:
	docker build --force-rm -f docker/Dockerfile.app -t zetsubou/app:0.0.1-python-3.8.16-slim-buster .
build-docker-airflow:
	docker build --force-rm -f docker/Dockerfile.airflow -t zetsubou/airflow:2.6.1-python3.8 .
build-docker-airflow-simple:
	docker build --force-rm -f docker/Dockerfile.airflow.simple -t zetsubou/airflow-simple:2.6.2-python3.8 .
build-dev: build-docker-airflow-simple
	poetry install
	source ./.venv/bin/activate; pre-commit install
build: build-docker-app build-docker-airflow-simple

lint:
	pre-commit run --all-files
	npx commitlint --from "HEAD~1" --to "HEAD" --verbose

.PHONY: init init-app-example init-app-postgres init-airflow init-app-elastic init-redis
init-app-elastic:
	mkdir -p $(ZETSUBOU_ELASTICSEARCH_VOLUME)
	chown -R 1000:1000 $(ZETSUBOU_ELASTICSEARCH_VOLUME)
init-app-postgres:
	mkdir -p $(ZETSUBOU_POSTGRES_DB_VOLUME)
init-app-example:
	docker-compose -f docker-compose.simple.yml up -d zetsubou-app-example
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

	docker-compose -f docker/docker-compose.host.airflow.yml up airflow-init
init-redis:
	mkdir -p $(ZETSUBOU_REDIS_VOLUME)
	chown -R 1001:1001 $(ZETSUBOU_REDIS_VOLUME)
init-example: init-app-postgres init-app-elastic init-minio init-redis init-app-example

.PHONY: clean clean-all clean-airflow clean-airflow-simple clean-app-elastic clean-app-postgres clean-docker
clean-airflow:
	rm -rf $(AIRFLOW_VOLUME)
clean-airflow-simple:
	rm -rf $(AIRFLOW_SIMPLE_VOLUME)
clean-app-elastic:
	rm -rf $(ZETSUBOU_ELASTICSEARCH_VOLUME)
clean-app-postgres:
	rm -rf $(ZETSUBOU_POSTGRES_DB_VOLUME)
clean-docker:
	docker rmi $(shell docker images -f "dangling=true" -q)
clean: clean-airflow-simple clean-docker

clean-all:
	rm -f ./.env
	rm -rf ./dev
	rm -rf ./etc
	rm -rf ./logs
	rm -rf ./statics
	rm -rf ./venv

.PHONY: reset-app reset-app-elastic reset-app-postgres reset-airflow-simple
reset-app-elastic: clean-app-elastic init-app-elastic
reset-app-postgres: clean-app-postgres init-app-postgres
reset-app: reset-app-elastic reset-app-postgres

reset-airflow-simple: clean-airflow-simple

.PHONY: up-app-simple up-airflow up-airflow-simple up-dev up
up-app-simple:
	docker-compose -f docker-compose.simple.yml up -d $(APP_SERVICES)
up-airflow:
	docker-compose -f docker/docker-compose.host.airflow.yml up -d
up-airflow-simple:
	docker-compose -f docker-compose.simple.yml up -d zetsubou-airflow
up-dev:
	docker-compose -f docker-compose.simple.yml up -d $(APP_DEV_SERVICES)
up: up-app-simple

.PHONY: down
down-simple:
	docker-compose -f docker-compose.simple.yml down
down-airflow:
	docker-compose -f docker/docker-compose.host.airflow.yml down
down: down-simple

.PHONY: logs
logs:
	docker-compose -f docker-compose.simple.yml logs $(service)

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt --without-hashes
