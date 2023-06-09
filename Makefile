SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: clean install

.PHONY: clean
clean: ## Removes project virtual env
	rm -rf .venv build dist **/*.egg-info .pytest_cache node_modules .coverage

.PHONY: install
install: ## Install the project dependencies and pre-commit using Poetry.
	poetry install
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

.PHONY: test
test: ## Run tests
	poetry run python -m pytest --cov=data_api_project --cov-report html

.PHONY: update
update: ## Run update poetry
	poetry update

.PHONY: start-airflow
start-airflow: ## Start Airflow
	docker build . -f ./airflow/Dockerfile --pull --tag airflow_modern_stack:latest
	docker-compose -f ./airflow/docker-compose.yaml up -d

.PHONY: down-airflow
down-airflow: ## Down Airflow
	docker-compose -f ./airflow/docker-compose.yaml down --remove-orphans

.PHONY: clone-airbyte
clone-airbyte:
	git clone https://github.com/airbytehq/airbyte.git

.PHONY:
start-airbyte:
	./airbyte/run-ab-platform.sh
