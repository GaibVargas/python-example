.PHONY: lint-check lint-fix lint format-check format-fix format import-check import-fix import type-check check-all test migrate migrate-head dev-server dev-scraping

# Lint
lint-check:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

lint: lint-fix

# Format
format-check:
	uv run black --check .

format-fix:
	uv run black .

format: format-fix

# Imports
import-check:
	uv run isort --check-only .

import-fix:
	uv run isort .

import: import-fix

# Type
type-check:
	uv run mypy src

check-all: import format lint type-check

# Test
test:
	uv run python -m unittest discover -s tests

# Migrations
migrate:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Uso: make automigrate 'nome da migration'"; \
	else \
		name="$(filter-out $@,$(MAKECMDGOALS))"; \
		timestamp=$$(date +'%Y%m%d%H%M%S'); \
		uv run alembic revision --autogenerate -m "$${timestamp}_$${name}"; \
	fi

migrate-head:
	uv run alembic upgrade head

# Dev run
dev-server:
	uv run uvicorn app.main:app --reload
	
dev-scraping:
	uv run src/tasks/scraping_cron.py

# Evita erro "Sem regra para processar o alvo"
%:
	@: