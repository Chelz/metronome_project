PORT=8000
APP_NAME=simple-aggregator-service

.PHONY: help

help: ## Current step
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


start-service: ## Start the simple aggregator service
	docker build -t $(APP_NAME) .
	docker run -it --rm -p "$(PORT):$(PORT)" --name="$(APP_NAME)" $(APP_NAME)

stop-service: ## Stop the simple aggregator service and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)
