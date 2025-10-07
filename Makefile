# Lint
.PHONY: lint-check lint-fix lint
lint-check:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

lint: lint-fix

# Format
.PHONY: format-check format-fix format
format-check:
	uv run black --check .

format-fix:
	uv run black .

format: format-fix

# Imports
.PHONY: import-check import-fix import
import-check:
	uv run isort --check-only .

import-fix:
	uv run isort .

import: import-fix

# Type
.PHONY: type-check
type-check:
	uv run mypy src

.PHONY: check-all
check-all: import format lint type-check

# Test
.PHONY: test
test:
	uv run python -m unittest discover -s tests

# Migrations
.PHONY: migrate migrate-head
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
.PHONY: dev
dev:
	uv run uvicorn app.main:app --reload

# Evita erro "Sem regra para processar o alvo"
%:
	@: