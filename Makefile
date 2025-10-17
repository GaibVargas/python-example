REGISTRY	?= registry.infe.dev.br/inferenciacms
IMAGE_REPO      ?= inferenciacms
IMAGE	   ?= $(REGISTRY)/$(IMAGE_REPO)

# Tags baseadas no commit atual (não sobrescrever) com GITHUB_SHA vindo do GitHub Actions ou git local
FULL_SHA := $(shell echo $${GITHUB_SHA:-$$(git rev-parse HEAD)}) # SHA completo do commit atual
SHORT_SHA := $(shell echo $${GITHUB_SHA:-$$(git rev-parse HEAD)} | cut -c1-7) # SHA curto (7 primeiros caracteres)

# Detecta se está rodando no WSL (Windows Subsystem for Linux)
IS_WSL := $(shell grep -qi microsoft /proc/version && echo true || echo false)

DB_DEV_CONTAINER=postgres
DB_DEV_USER=postgres
DB_DEV_DB=python_example

DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKERFILE_PROD_API=Dockerfile.api
DOCKERFILE_PROD_SCRAPING=Dockerfile.scraping

.PHONY: prehook lint_check lint_fix format_check format_fix import_check import_fix type_check fix_all lint
.PHONY: test_unit migrate migrate_head start run run_scraping stop reset psql db_verify

lint_check lint_fix format_check format_fix import_check import_fix type_check fix_all lint: prehook

test_unit migrate migrate_head start run run_scraping stop reset psql db_verify: prehook

prehook:
	@if [ "$(IS_WSL)" = "true" ]; then \
		echo ">>> 🪟  Executando no WSL\033[0m"; \
	else \
		echo ">>> 🐧  Executando em Linux Nativo"; \
	fi


# Lint
lint_check:
	uv run ruff check .

lint_fix:
	uv run ruff check . --fix

# Format
format_check:
	uv run black --check .

format_fix:
	uv run black .

# Imports
import_check:
	uv run isort --check-only .

import_fix:
	uv run isort .

# Type
type_check:
	uv run mypy src

# Corrige todas os problemas de lint, formatação, e imports
fix_all: import_fix format_fix lint_fix type_check

# Verifica todos os problemas de lint, formatação, imports e tipos
lint: import_check format_check lint_check type_check

# Migrations
# Cria uma nova migration com timestamp no nome
migrate:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Uso: make automigrate 'nome da migration'"; \
	else \
		name="$(filter-out $@,$(MAKECMDGOALS))"; \
		timestamp=$$(date +'%Y%m%d%H%M%S'); \
		uv run alembic revision --autogenerate -m "$${timestamp}_$${name}"; \
	fi

# Aplica todas as migrations pendentes
migrate_head:
	uv run alembic upgrade head

# Test
test_unit:
	@echo ">>> 🧪  Rodando testes unitários..."
	uv run python -m unittest discover -s tests/unit

test_integration:
	@echo ">>> 🧪  Rodando testes de integração..."
	uv run python -m unittest discover -s tests/integration

# Inicia contêineres locais para desenvolvimento
start:
	@echo ">>> 🚀  Iniciando contêineres PostgreSQL locais..."
	@docker compose -f $(DOCKER_COMPOSE_DEV_FILE) up -d
	@echo ">>> ⏳  Aguardando PostgreSQL iniciar dentro do contêiner..."
	@until [ "$$(docker inspect -f '{{.State.Health.Status}}' $(DB_DEV_CONTAINER))" = "healthy" ]; do \
		sleep 1; \
	done
	@echo ">>> ✅  PostgreSQL pronto!"

# Verifica disponibilidade do banco de dados
db_verify:
	@echo ">>> 🚀  Verificando se o PostgreSQL está disponível..."
	@docker exec $(DB_DEV_CONTAINER) bash -c 'until pg_isready -U $(DB_DEV_USER) -d $(DB_DEV_DB); do sleep 1; done'
	@echo ">>> ✅  PostgreSQL está disponível!"

# Inicia a aplicação FastAPI localmente
run:
	@make db_verify
	@echo ">>> ☕  Iniciando aplicação FastAPI..."
	@uv run uvicorn app.main:app --reload

# Inicia o cron de scraping localmente
run_scraping:
	@make db_verify
	@echo ">>> ☕  Iniciando Cron de Scraping..."
	@uv run src/tasks/scraping_cron.py

# Para o contêineres locais
stop:
	@echo ">>> 🛑  Parando contêineres locais..."
	@docker compose -f $(DOCKER_COMPOSE_DEV_FILE) down
	@echo ">>> 🛑  Contêineres parados."

# Reseta o volume do banco de dados local
# (remove todos os dados do banco de dados)
reset:
	@echo ">>> 🗑️  Removendo volume e dados dos contêineres locais..."
	@docker compose -f docker-compose.dev.yml down -v
	@echo ">>> 🗑️  Volume e dados dos contêineres locais removidos."
	@make start
	@make run

# Inicia uma sessão de terminal no contêiner PostgreSQL local
psql:
	@echo ">>> 🖥️  Iniciando sessão de terminal no contêiner PostgreSQL local..."
	@docker exec -it $(DB_DEV_CONTAINER) psql -U $(DB_DEV_USER) -d $(DB_DEV_DB)

# Evita erro "Sem regra para processar o alvo"
%:
	@:


# (DESENVOLVEDORES NÃO PRECISAM | EXCLUSIVO DE CI)
# Faz login em nosso registry privado
login:
	@echo ">>> 🔐 Fazendo login em $(REGISTRY)"
	@echo '$(REGISTRY_TOKEN)' | docker login $(REGISTRY) -u "robot\$$$(REGISTRY_USER)" --password-stdin
#								                            ^ Necessário escapar $. então setar como 'inferenciacms-github' por ex

# Guard para garantir que TAG está setada
check-tag:
	@if [ -z "$(TAG)" ]; then \
		echo "❌ TAG não configurada. Uso: make $@ TAG=snapshot-s8-1"; \
		exit 1; \
	fi

# Faz build da imagem de produção
build: check-tag
	@echo ">>> 🛠 Buildando imagem $(IMAGE)"
	docker buildx build \
		--platform linux/amd64 \
		--label org.opencontainers.image.version=$(TAG) \
		--label org.opencontainers.image.revision=$(FULL_SHA) \
		-t $(IMAGE):$(TAG) \
		-t $(IMAGE):sha-$(SHORT_SHA) \
		-f $(DOCKERFILE_PROD) .

# Faz push da imagem para o registry
push: check-tag
	@echo ">>> 📤 Fazendo push da imagem $(IMAGE)"
	docker push $(IMAGE):$(TAG)
	docker push $(IMAGE):sha-$(SHORT_SHA)

# Faz deploy da imagem para o servidor de homologação
deploy: check-tag
	@if [ -z "$(HOST)" ]; then \
		echo "❌ HOST não configurada. Uso: make $@ HOST=192.0.0.1"; \
		exit 1; \
	fi
	@if [ -z "$(USER)" ]; then \
		echo "❌ USER não configurada. Uso: make $@ USER=deploy"; \
		exit 1; \
	fi
	@if [ -z "$(SSH_KEY)" ]; then \
		echo "❌ SSH_KEY não configurada. Uso: make $@ SSH_KEY=~/.ssh/id_rsa"; \
		exit 1; \
	fi
	@echo ">>> 🚀 Fazendo deploy de $(IMAGE):sha-$(SHORT_SHA) para servidor"
	ssh -i $(SSH_KEY) \
		-o StrictHostKeyChecking=no \
		$(USER)@$(HOST) \
		"sudo /usr/local/bin/deploy-service.sh inferenciacms $(IMAGE_REPO) $(IMAGE):$(TAG)"