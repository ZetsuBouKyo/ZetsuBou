-include ./etc/settings.env
export

SHELL := /bin/bash
ZETSUBOU_TIMESTAMP ?= $(shell date +'%Y-%m-%d-%H%M')
ZETSUBOU_APP_VERSION ?= 0.0.1
ZETSUBOU_ELASTICSEARCH_VOLUME ?= ./dev/volumes/elasticsearch
ZETSUBOU_ELASTICSEARCH_ANALYSIS_VOLUME ?= ./etc/analysis
ZETSUBOU_REDIS_VOLUME ?= ./dev/volumes/redis
ZETSUBOU_POSTGRES_DB_VOLUME ?= ./dev/volumes/postgres

APP_SERVICES := zetsubou-app zetsubou-airflow zetsubou-elasticsearch zetsubou-minio zetsubou-postgres zetsubou-redis
APP_DEV_SERVICES := zetsubou-airflow zetsubou-elasticsearch zetsubou-minio zetsubou-postgres zetsubou-redis

.PHONY: test line check

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

check:
	@docker > /dev/null 2>&1
	@docker-compose > /dev/null 2>&1
check-dev:
	@poetry > /dev/null 2>&1
	@docker > /dev/null 2>&1
	@docker-compose > /dev/null 2>&1
	@npm --version > /dev/null 2>&1

.PHONY: clean clean-all clean-airflow clean-airflow-simple clean-app-elasticsearch clean-app-postgres clean-docker
clean-airflow-simple:
	rm -rf $(ZETSUBOU_AIRFLOW_SIMPLE_VOLUME)
clean-app-elasticsearch:
	rm -rf $(ZETSUBOU_ELASTICSEARCH_VOLUME)
clean-app-postgres:
	rm -rf $(ZETSUBOU_POSTGRES_DB_VOLUME)
clean-docker:
	docker rmi $(shell docker images -f "dangling=true" -q)
clean-folders:
	rm -rf ./dev
	rm -rf ./etc
	rm -rf ./logs
	rm -rf ./statics
	rm -rf ./venv
clean: clean-folders clean-docker

.PHONY: docs
docs:
	mkdocs build
	npx prettier --write front/doc_site/
.PHONY: down
down:
	docker-compose -f docker-compose.simple.yml down

line:
	git ls-files | xargs wc -l || true
lint:
	pre-commit run --all-files
	npx commitlint --from "HEAD~1" --to "HEAD" --verbose
.PHONY: logs
logs:
	docker-compose -f docker-compose.simple.yml logs $(service)

.PHONY: init init-app-postgres init-app-elasticsearch init-redis
init-app-elasticsearch:
	mkdir -p $(ZETSUBOU_ELASTICSEARCH_VOLUME)
	mkdir -p $(ZETSUBOU_ELASTICSEARCH_ANALYSIS_VOLUME)
	chown -R 1000:1000 $(ZETSUBOU_ELASTICSEARCH_VOLUME)
	touch $(ZETSUBOU_ELASTICSEARCH_ANALYSIS_VOLUME)/synonym.txt
init-app-postgres:
	mkdir -p $(ZETSUBOU_POSTGRES_DB_VOLUME)
init-redis:
	mkdir -p $(ZETSUBOU_REDIS_VOLUME)
	chown -R 1001:1001 $(ZETSUBOU_REDIS_VOLUME)
init: init-app-postgres init-app-elasticsearch init-redis

pip-new:
	poetry show -o

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

.PHONY: reset-app reset-app-elasticsearch reset-app-postgres reset-airflow-simple
reset-app-elasticsearch: clean-app-elasticsearch init-app-elasticsearch
reset-app-postgres: clean-app-postgres init-app-postgres
reset-app: reset-app-elasticsearch reset-app-postgres

reset-airflow-simple: clean-airflow-simple

.PHONY: start-airflow
start-airflow:
	docker-compose -f docker-compose.simple.yml start zetsubou-airflow
.PHONY: stop-airflow
stop-airflow:
	docker-compose -f docker-compose.simple.yml stop zetsubou-airflow

test:
	echo "$(ZETSUBOU_TIMESTAMP)"

.PHONY: tests-cov
tests-cov:
	pytest --cov=. --cov-report term-missing tests/

.PHONY: up-app-simple up-airflow-simple up-dev up
up-airflow-simple:
	docker-compose -f docker-compose.simple.yml up -d zetsubou-airflow
up-app-simple:
	docker-compose -f docker-compose.simple.yml up -d $(APP_SERVICES)
up-dev:
	docker-compose -f docker-compose.simple.yml up -d $(APP_DEV_SERVICES)
up: up-app-simple
