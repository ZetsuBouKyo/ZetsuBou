-include ./etc/settings.env
export

SHELL := /bin/bash
ZETSUBOU_TIMESTAMP ?= $(shell date +'%Y-%m-%d-%H%M')
ZETSUBOU_APP_VERSION ?= 0.0.1
ZETSUBOU_ELASTICSEARCH_VOLUME ?= ./dev/volumes/elasticsearch
ZETSUBOU_ELASTICSEARCH_ANALYSIS_VOLUME ?= ./etc/analysis
ZETSUBOU_REDIS_VOLUME ?= ./dev/volumes/redis
ZETSUBOU_POSTGRES_DB_VOLUME ?= ./dev/volumes/postgres

APP_STANDALONE_SERVICES := zetsubou-airflow-standalone zetsubou-elasticsearch zetsubou-minio zetsubou-postgres zetsubou-redis

.PHONY: test line check

.PHONY: build build-docker-app build-docker-airflow build-docker-airflow-standalone build-dev
build-docker-app:
	docker build --force-rm -f docker/Dockerfile.app -t zetsuboukyo/app:0.0.1-python-3.8.16-slim-buster .
build-docker-airflow:
	docker build --force-rm -f docker/Dockerfile.airflow -t zetsuboukyo/airflow:2.6.1-python3.8 .
build-docker-airflow-standalone:
	docker build --force-rm -f docker/Dockerfile.airflow.standalone -t zetsuboukyo/airflow-standalone:2.6.2-python3.8 .
build-dev: build-docker-airflow-standalone
	poetry install
	source ./.venv/bin/activate; pre-commit install
build: build-docker-app build-docker-airflow-standalone

check:
	@docker > /dev/null 2>&1
	@docker-compose > /dev/null 2>&1
check-dev:
	@poetry > /dev/null 2>&1
	@docker > /dev/null 2>&1
	@docker-compose > /dev/null 2>&1
	@npm --version > /dev/null 2>&1

.PHONY: clean clean-all clean-airflow clean-airflow-standalone clean-app-elasticsearch clean-app-postgres clean-docker
clean-airflow-standalone:
	rm -rf $(ZETSUBOU_AIRFLOW_STANDALONE_VOLUME)
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
	docker-compose -f docker-compose.standalone.yml down

line:
	git ls-files | xargs wc -l || true
lint:
	pre-commit run --all-files
	npx commitlint --from "HEAD~1" --to "HEAD" --verbose
.PHONY: logs
logs:
	docker-compose -f docker-compose.standalone.yml logs $(service)

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

.PHONY: ping pip-new pip-list
ping:
	python cli.py test service ping
pip-new:
	poetry show -o
pip-list:
	./scripts/pip-list

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt --without-hashes

.PHONY: reset-app reset-app-elasticsearch reset-app-postgres reset-airflow-standalone
reset-app-elasticsearch: clean-app-elasticsearch init-app-elasticsearch
reset-app-postgres: clean-app-postgres init-app-postgres
reset-app: reset-app-elasticsearch reset-app-postgres

reset-airflow-standalone: clean-airflow-standalone

.PHONY: start-airflow-standalone
start-airflow-standalone:
	docker-compose -f docker-compose.standalone.yml start zetsubou-airflow-standalone
.PHONY: stop-airflow-standalone
stop-airflow-standalone:
	docker-compose -f docker-compose.standalone.yml stop zetsubou-airflow-standalone

test:
	echo "$(ZETSUBOU_TIMESTAMP)"

.PHONY: tests-cov tests-not-integration
tests-cov:
	pytest --cov=back --cov=command --cov=dags --cov=lib --cov=tests --cov-report term-missing tests/
tests-cov-not-gen:
	pytest -m "not gen" --cov=back --cov=command --cov=dags --cov=lib --cov=tests --cov-report term-missing tests/
tests-cov-not-integration:
	pytest -m "not integration" --cov=back --cov=command --cov=dags --cov=lib --cov=tests --cov-report term-missing tests/

.PHONY: up-airflow-standalone up-standalone up
up-airflow-standalone:
	docker-compose -f docker-compose.standalone.yml up -d zetsubou-airflow-standalone
up-standalone:
	docker-compose -f docker-compose.standalone.yml up -d $(APP_STANDALONE_SERVICES)
up: up-standalone
