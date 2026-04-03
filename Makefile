# Entry point: .env setup, Alembic revisions/migrations, and Docker Compose.
# Examples: make help | make dev | make migrate | make up ARGS=-d

SHELL := /bin/bash
.DEFAULT_GOAL := help

ROOT := $(abspath .)
DC := docker compose -f $(ROOT)/compose.yml
ALEMBIC_CFG := migrations/alembic.ini

.PHONY: help setup env migration migrate dev compose up down build logs ps

help: ## Show available targets
	@echo "Chronos — Makefile targets"
	@echo ""
	@echo "  make setup       Generate .env at repo root (scripts/create_enviroment_setup.sh)"
	@echo "  make env         Alias for setup"
	@echo "  make migration   New Alembic revision (scripts/create_migration.sh, interactive)"
	@echo "  make migrate     Apply migrations to the database (alembic upgrade head)"
	@echo ""
	@echo "  make dev         Docker Compose up -d with rebuild (detached)"
	@echo "  make up          docker compose up (e.g. make up ARGS=-d)"
	@echo "  make down        docker compose down"
	@echo "  make build       docker compose build"
	@echo "  make logs        docker compose logs -f"
	@echo "  make ps          docker compose ps"
	@echo "  make compose     Pass any subcommand: make compose ARGS=\"exec api bash\""
	@echo ""
	@echo "  migrate uses POSTGRES_HOST=localhost by default (host -> published DB port)."
	@echo "  Override: make migrate POSTGRES_HOST=postgres (e.g. from another container)."
	@echo ""

setup: ## Write .env (secrets and vars for Compose / pydantic-settings)
	bash "$(ROOT)/scripts/create_enviroment_setup.sh"

env: setup ## Alias for setup

migration: ## Create Alembic revision with date/time file prefix (interactive)
	bash "$(ROOT)/scripts/create_migration.sh"

migrate: ## Apply Alembic migrations (upgrade head; host dev defaults POSTGRES_HOST to localhost)
	cd "$(ROOT)" && \
	POSTGRES_HOST="$${POSTGRES_HOST:-localhost}" \
	uv run alembic -c "$(ALEMBIC_CFG)" upgrade head

dev: ## Local dev: Compose up detached with rebuild (use make logs to follow output)
	$(DC) up -d --build $(ARGS)

compose: ## Forward args to docker compose (e.g. ARGS="up -d --build")
	$(DC) $(ARGS)

up: ## Start services (optional ARGS, e.g. -d)
	$(DC) up $(ARGS)

down: ## Stop services
	$(DC) down $(ARGS)

build: ## Build images from compose file
	$(DC) build $(ARGS)

logs: ## Follow logs (optional ARGS: service name)
	$(DC) logs -f $(ARGS)

ps: ## List project containers
	$(DC) ps $(ARGS)
