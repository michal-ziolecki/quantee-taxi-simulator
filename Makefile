.PHONY: \
	init-env \
	build \
	build-and-run \
	rebuild-and-run \
	run \
	stop \
	stop-all \
	clean-unused-images \
	clean-all-images \
	clean-unused-containers \
	clean-all-containers \
	clean-db-data \
	clean-unused-volumes \
	clean-all-volumes \
	clean-up \
	clean \
	prune \
	poetry-update \
	install-deps \
	list-volumes \
	styling \
	static-tests \
	migration \
	migrate-up \
	migration-history \
	migration-current \
	migrate-down \
	give-migrations-permission \
	logs \
	help



DOCKER ?= docker
COMPOSE ?= docker-compose
POETRY ?= poetry
BE_CONTAINER_NAME ?= dispatcher
ALEMBIC_CONFIG ?= /dispatcher/db/alembic.ini
PWD ?= $(shell pwd)

-include .env

help:
	@echo "Usage:"
	@echo ""
	@echo "  init-env:                    Create .env file from .env.template"
	@echo "  build:                       Build the docker images"
	@echo "  build-and-run:               Build and run containers"
	@echo "  rebuild-and-run:             Rebuild and run containers (force recreate)"
	@echo "  run:                         Start the containers"
	@echo "  stop:                        Stop and remove containers"
	@echo "  stop-all:                    Stop all running containers"
	@echo "  clean-unused-images:         Remove dangling images"
	@echo "  clean-all-images:            Remove all Docker images"
	@echo "  clean-unused-containers:     Remove exited containers"
	@echo "  clean-all-containers:        Remove all containers"
	@echo "  clean-db-data:               Remove named volume 'quantee_data'"
	@echo "  clean-unused-volumes:        Remove dangling volumes"
	@echo "  clean-all-volumes:           Remove all volumes and 'quantee_datae'"
	@echo "  clean-up:                    Clean unused containers, images, and volumes"
	@echo "  clean:                       Full cleanup: containers, images, volumes"
	@echo "  prune:                       Prune everything: system, images, networks, volumes"
	@echo "  poetry-update:               Update Poetry to version 2.1.3"
	@echo "  install-deps:                Install Python dependencies with Poetry"
	@echo "  list-volumes:                List Docker volumes"
	@echo "  styling:                     Run code style checks"
	@echo "  static-tests:                Run static analysis checks"
	@echo "  migration:                   Create a new migration (use title=...)"
	@echo "  migrate-up:                  Apply latest DB migrations"
	@echo "  migration-history:           Show Alembic migration history"
	@echo "  migration-current:           Show current Alembic migration"
	@echo "  migrate-down:                Revert to a specific migration (use version=...)"
	@echo "  give-migrations-permission:  Fix migration folder permissions"
	@echo "  logs:                        Tail logs from the backend container"


init-env:
	@echo "Creating .env file from .env.template"
	@cp .env.template .env
	@echo "Please fill in the required values in the .env file."

build:
	$(COMPOSE) build --parallel

build-and-run:
	$(COMPOSE) up -d --build

rebuild-and-run:
	$(COMPOSE) up -d --build --force-recreate

run:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down --remove-orphans

stop-all:
	$(DOCKER) ps -q | xargs -r $(DOCKER) stop

clean-unused-images:
	$(DOCKER) images -f "dangling=true" -q | xargs -r $(DOCKER) rmi -f

clean-all-images:
	$(DOCKER) images -q | xargs -r $(DOCKER) rmi -f

clean-unused-containers:
	$(DOCKER) ps -a -f "status=exited" -q | xargs -r $(DOCKER) rm -f

clean-all-containers:
	$(DOCKER) container ls -a -q | xargs -r $(DOCKER) rm -f

clean-db-data:
	$(DOCKER) volume rm quantee_data

clean-unused-volumes:
	$(DOCKER) volume ls -qf dangling=true | xargs -r $(DOCKER) volume rm

clean-all-volumes:
	$(DOCKER) volume prune -f
	$(DOCKER) volume rm quantee_datae

clean-up: clean-unused-containers clean-unused-images clean-unused-volumes

clean: stop clean-all-containers clean-all-images clean-all-volumes

prune:
	$(DOCKER) system prune -a -f
	$(DOCKER) volume rm quantee_datae

poetry-update:
	$(POETRY) self update 2.1.3

install-deps:
	$(POETRY) install

list-volumes:
	$(DOCKER) volume ls

styling:
	./run_code_styling.sh

static-tests:
	./tests/static_analysis/static_analysis_test.sh

migration:
	@if [ -z "$(title)" ]; then \
		echo "Error: You must provide a title for the migration by argument title=name" && exit 1; \
	fi
	$(DOCKER) exec -it $(BE_CONTAINER_NAME) bash -c "export ALEMBIC_CONFIG=$(ALEMBIC_CONFIG) && alembic revision -m '$(title)'"

migrate-up:
	$(DOCKER) exec -it $(BE_CONTAINER_NAME) bash -c "export ALEMBIC_CONFIG=$(ALEMBIC_CONFIG) && alembic upgrade head"

migration-history:
	$(DOCKER) exec -it $(BE_CONTAINER_NAME) bash -c "export ALEMBIC_CONFIG=$(ALEMBIC_CONFIG) && alembic history"

migration-current:
	$(DOCKER) exec -it $(BE_CONTAINER_NAME) bash -c "export ALEMBIC_CONFIG=$(ALEMBIC_CONFIG) && alembic current"

migrate-down:
	@if [ -z "$(version)" ]; then \
		echo "Error: You must provide a version to downgrade to by argument version=hashid" && exit 1; \
	fi
	$(DOCKER) exec -it $(BE_CONTAINER_NAME) bash -c "export ALEMBIC_CONFIG=$(ALEMBIC_CONFIG) && alembic downgrade $(version)"

give-migrations-permission:
	$(DOCKER) exec -u root -it $(BE_CONTAINER_NAME) bash -c "chmod -R 777 /code/api/migrations"

logs:
	$(DOCKER) logs -f --tail 100 $(BE_CONTAINER_NAME)
