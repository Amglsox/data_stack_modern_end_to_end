.PHONY: build-api
build-api: ## Build API
	cp poetry.lock pyproject.toml ./generate_data_python && cd ./generate_data_python && docker build . -t generate-data-api:latest && rm -rf poetry.lock pyproject.toml

.PHONY: start-api
start-api: ## Start API
	docker run --name generate_data_api generate-data-api:latest && docker rm generate_data_api
