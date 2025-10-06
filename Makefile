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
	uv run mypy

.PHONY: check-all
check-all: import format lint type-check

# Test
.PHONY: test
test:
	uv run python -m unittest discover -s tests