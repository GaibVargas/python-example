#!/bin/sh
set -e

export APP_HOST=${APP_HOST:-0.0.0.0}
export APP_PORT=${APP_PORT:-8000}

echo "🏗️ Rodando migrations Alembic..."
uv run alembic upgrade head

echo "🚀 Iniciando aplicação FastAPI em ${APP_HOST}:${APP_PORT}..."
exec uv run uvicorn app.main:app --host $APP_HOST --port $APP_PORT --log-config src/infra/logger/logger_config.json --no-use-colors
