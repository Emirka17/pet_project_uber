# ============================================================================
# PET PROJECT UBER - Makefile
# ============================================================================

.PHONY: help up down logs ps clean rebuild \
        k8s-up k8s-down k8s-status k8s-logs \
        minikube-start minikube-stop minikube-dashboard \
        migrate seed shell-postgres shell-redis \
        test test-integration test-load \
        build lint format

# Цвета для вывода
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
BLUE   := \033[0;34m
NC     := \033[0m # No Color

# Переменные
DOCKER_COMPOSE := docker compose
KUBECTL := kubectl
NAMESPACE := uber

# ============================================================================
# HELP
# ============================================================================

help: ## Показать справку
	@echo ""
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║              PET PROJECT UBER - Команды                        ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Docker Compose:$(NC)"
	@grep -E '^(up|down|logs|ps|clean|rebuild|restart|stop|start):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Kubernetes:$(NC)"
	@grep -E '^k8s-[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Minikube:$(NC)"
	@grep -E '^minikube-[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)База данных:$(NC)"
	@grep -E '^(migrate|seed|shell-[a-zA-Z_-]+|db-[a-zA-Z_-]+):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Kafka:$(NC)"
	@grep -E '^kafka-[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Тесты:$(NC)"
	@grep -E '^test[a-zA-Z_-]*:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Сборка и линтинг:$(NC)"
	@grep -E '^(build|build-[a-zA-Z_-]+|push|lint|format):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Утилиты:$(NC)"
	@grep -E '^(health|generate-data|docs-serve|install-deps|info):.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# DOCKER COMPOSE
# ============================================================================

up: ## Запустить все сервисы
	@echo "$(BLUE)▶ Запуск сервисов...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ Все сервисы запущены$(NC)"
	@echo ""
	@echo "$(YELLOW)Доступные UI:$(NC)"
	@echo "  Kafka UI:    http://localhost:9093"
	@echo "  Metabase:    http://localhost:3000"
	@echo "  ClickHouse:  http://localhost:8123"

down: ## Остановить все сервисы
	@echo "$(BLUE)▶ Остановка сервисов...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Все сервисы остановлены$(NC)"

logs: ## Показать логи всех сервисов
	$(DOCKER_COMPOSE) logs -f

logs-service: ## Показать логи конкретного сервиса (make logs-service s=user-service)
	$(DOCKER_COMPOSE) logs -f $(s)

ps: ## Показать статус сервисов
	@echo "$(BLUE)▶ Статус сервисов:$(NC)"
	@echo ""
	$(DOCKER_COMPOSE) ps

clean: ## Остановить и удалить всё (контейнеры, volumes, networks)
	@echo "$(RED)▶ Удаление всех ресурсов...$(NC)"
	$(DOCKER_COMPOSE) down -v --rmi local --remove-orphans
	@echo "$(GREEN)✓ Очистка завершена$(NC)"

rebuild: ## Пересобрать и перезапустить все сервисы
	@echo "$(BLUE)▶ Пересборка сервисов...$(NC)"
	$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)✓ Сервисы пересобраны и запущены$(NC)"

restart: ## Перезапустить все сервисы
	@echo "$(BLUE)▶ Перезапуск сервисов...$(NC)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)✓ Сервисы перезапущены$(NC)"

stop: ## Остановить сервисы без удаления
	$(DOCKER_COMPOSE) stop

start: ## Запустить остановленные сервисы
	$(DOCKER_COMPOSE) start

# ============================================================================
# KUBERNETES
# ============================================================================

k8s-up: ## Развернуть приложение в Kubernetes
	@echo "$(BLUE)▶ Разворачивание в Kubernetes...$(NC)"
	$(KUBECTL) apply -k k8s/
	@echo "$(GREEN)✓ Ресурсы созданы$(NC)"
	@echo ""
	@make k8s-status

k8s-down: ## Удалить приложение из Kubernetes
	@echo "$(RED)▶ Удаление из Kubernetes...$(NC)"
	$(KUBECTL) delete -k k8s/ --ignore-not-found
	@echo "$(GREEN)✓ Ресурсы удалены$(NC)"

k8s-status: ## Показать статус ресурсов в Kubernetes
	@echo "$(BLUE)▶ Статус Kubernetes:$(NC)"
	@echo ""
	@echo "$(YELLOW)━━━ Namespace ━━━$(NC)"
	@$(KUBECTL) get ns $(NAMESPACE) 2>/dev/null || echo "Namespace $(NAMESPACE) не найден"
	@echo ""
	@echo "$(YELLOW)━━━ Pods ━━━$(NC)"
	@$(KUBECTL) get pods -n $(NAMESPACE) 2>/dev/null || echo "Нет подов"
	@echo ""
	@echo "$(YELLOW)━━━ Services ━━━$(NC)"
	@$(KUBECTL) get svc -n $(NAMESPACE) 2>/dev/null || echo "Нет сервисов"
	@echo ""
	@echo "$(YELLOW)━━━ Deployments ━━━$(NC)"
	@$(KUBECTL) get deployments -n $(NAMESPACE) 2>/dev/null || echo "Нет деплойментов"

k8s-logs: ## Показать логи пода (make k8s-logs app=user-service)
	$(KUBECTL) logs -f -n $(NAMESPACE) -l app=$(app)

k8s-describe: ## Описать под (make k8s-describe app=user-service)
	$(KUBECTL) describe pod -n $(NAMESPACE) -l app=$(app)

k8s-shell: ## Открыть shell в поде (make k8s-shell app=user-service)
	$(KUBECTL) exec -it -n $(NAMESPACE) deployment/$(app) -- /bin/sh

k8s-port-forward: ## Проброс портов для локального доступа
	@echo "$(BLUE)▶ Проброс портов...$(NC)"
	@echo "PostgreSQL: localhost:5432"
	@echo "Redis:      localhost:6379"
	@echo "Kafka:      localhost:9092"
	@echo ""
	@echo "$(YELLOW)Нажмите Ctrl+C для остановки$(NC)"
	@$(KUBECTL) port-forward -n $(NAMESPACE) svc/postgres 5432:5432 &
	@$(KUBECTL) port-forward -n $(NAMESPACE) svc/redis 6379:6379 &
	@$(KUBECTL) port-forward -n $(NAMESPACE) svc/kafka 9092:9092 &
	@wait

k8s-restart: ## Перезапустить deployment (make k8s-restart app=user-service)
	$(KUBECTL) rollout restart deployment/$(app) -n $(NAMESPACE)

# ============================================================================
# MINIKUBE
# ============================================================================

minikube-start: ## Запустить Minikube
	@echo "$(BLUE)▶ Запуск Minikube...$(NC)"
	minikube start --memory=4096 --cpus=2 --driver=docker
	minikube addons enable ingress
	minikube addons enable metrics-server
	@echo "$(GREEN)✓ Minikube запущен$(NC)"

minikube-stop: ## Остановить Minikube
	@echo "$(BLUE)▶ Остановка Minikube...$(NC)"
	minikube stop
	@echo "$(GREEN)✓ Minikube остановлен$(NC)"

minikube-delete: ## Удалить Minikube кластер
	@echo "$(RED)▶ Удаление Minikube...$(NC)"
	minikube delete
	@echo "$(GREEN)✓ Minikube удалён$(NC)"

minikube-dashboard: ## Открыть Minikube Dashboard
	minikube dashboard

minikube-ip: ## Показать IP Minikube
	@echo "$(BLUE)Minikube IP:$(NC) $$(minikube ip)"

minikube-ssh: ## SSH в Minikube
	minikube ssh

# ============================================================================
# DATABASE
# ============================================================================

migrate: ## Применить миграции БД
	@echo "$(BLUE)▶ Применение миграций...$(NC)"
	./scripts/run_migrations.sh
	@echo "$(GREEN)✓ Миграции применены$(NC)"

seed: ## Загрузить тестовые данные
	@echo "$(BLUE)▶ Загрузка тестовых данных...$(NC)"
	python scripts/generate_data.py
	@echo "$(GREEN)✓ Данные загружены$(NC)"

shell-postgres: ## Подключиться к PostgreSQL
	@echo "$(BLUE)▶ Подключение к PostgreSQL...$(NC)"
	$(DOCKER_COMPOSE) exec postgres psql -U uber -d uber

shell-redis: ## Подключиться к Redis CLI
	@echo "$(BLUE)▶ Подключение к Redis...$(NC)"
	$(DOCKER_COMPOSE) exec redis redis-cli

shell-clickhouse: ## Подключиться к ClickHouse
	@echo "$(BLUE)▶ Подключение к ClickHouse...$(NC)"
	$(DOCKER_COMPOSE) exec clickhouse clickhouse-client

db-backup: ## Создать бэкап PostgreSQL
	@echo "$(BLUE)▶ Создание бэкапа...$(NC)"
	$(DOCKER_COMPOSE) exec postgres pg_dump -U uber uber > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Бэкап создан$(NC)"

db-reset: ## Сбросить базу данных
	@echo "$(RED)▶ Сброс базы данных...$(NC)"
	$(DOCKER_COMPOSE) exec postgres psql -U uber -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@make migrate
	@echo "$(GREEN)✓ База сброшена$(NC)"

# ============================================================================
# KAFKA
# ============================================================================

kafka-topics: ## Создать топики Kafka
	@echo "$(BLUE)▶ Создание топиков Kafka...$(NC)"
	./scripts/create_kafka_topics.sh
	@echo "$(GREEN)✓ Топики созданы$(NC)"

kafka-list-topics: ## Показать список топиков
	$(DOCKER_COMPOSE) exec kafka kafka-topics --list --bootstrap-server localhost:9092

kafka-describe-topic: ## Описать топик (make kafka-describe-topic t=rides)
	$(DOCKER_COMPOSE) exec kafka kafka-topics --describe --topic $(t) --bootstrap-server localhost:9092

kafka-consume: ## Читать сообщения из топика (make kafka-consume t=rides)
	$(DOCKER_COMPOSE) exec kafka kafka-console-consumer --topic $(t) --bootstrap-server localhost:9092 --from-beginning

# ============================================================================
# TESTS
# ============================================================================

test: ## Запустить все unit тесты
	@echo "$(BLUE)▶ Запуск unit тестов...$(NC)"
	pytest tests/ -v --ignore=tests/integration --ignore=tests/load --ignore=tests/e2e
	@echo "$(GREEN)✓ Тесты завершены$(NC)"

test-integration: ## Запустить интеграционные тесты
	@echo "$(BLUE)▶ Запуск интеграционных тестов...$(NC)"
	pytest tests/integration/ -v
	@echo "$(GREEN)✓ Интеграционные тесты завершены$(NC)"

test-e2e: ## Запустить e2e тесты
	@echo "$(BLUE)▶ Запуск e2e тестов...$(NC)"
	pytest tests/e2e/ -v
	@echo "$(GREEN)✓ E2E тесты завершены$(NC)"

test-load: ## Запустить нагрузочные тесты (Locust)
	@echo "$(BLUE)▶ Запуск нагрузочных тестов...$(NC)"
	cd tests/load && locust -f locustfile.py

test-coverage: ## Запустить тесты с покрытием
	@echo "$(BLUE)▶ Запуск тестов с покрытием...$(NC)"
	pytest tests/ --cov=services --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Отчёт о покрытии: htmlcov/index.html$(NC)"

test-all: test test-integration test-e2e ## Запустить все тесты

# ============================================================================
# BUILD
# ============================================================================

build: ## Собрать все Docker образы
	@echo "$(BLUE)▶ Сборка Docker образов...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✓ Образы собраны$(NC)"

build-service: ## Собрать конкретный сервис (make build-service s=user-service)
	@echo "$(BLUE)▶ Сборка $(s)...$(NC)"
	$(DOCKER_COMPOSE) build $(s)
	@echo "$(GREEN)✓ $(s) собран$(NC)"

push: ## Запушить образы в registry
	@echo "$(BLUE)▶ Публикация образов...$(NC)"
	$(DOCKER_COMPOSE) push
	@echo "$(GREEN)✓ Образы опубликованы$(NC)"

# ============================================================================
# LINT & FORMAT
# ============================================================================

lint: ## Проверить код линтерами
	@echo "$(BLUE)▶ Проверка Python кода...$(NC)"
	flake8 services/ --max-line-length=120
	@echo "$(BLUE)▶ Проверка Go кода...$(NC)"
	cd services/api-gateway && go vet ./...
	cd services/matching-service && go vet ./...
	cd services/geo-service && go vet ./...
	@echo "$(GREEN)✓ Линтинг завершён$(NC)"

format: ## Отформатировать код
	@echo "$(BLUE)▶ Форматирование Python кода...$(NC)"
	black services/ --line-length=120
	isort services/
	@echo "$(BLUE)▶ Форматирование Go кода...$(NC)"
	cd services/api-gateway && go fmt ./...
	cd services/matching-service && go fmt ./...
	cd services/geo-service && go fmt ./...
	@echo "$(GREEN)✓ Форматирование завершено$(NC)"

# ============================================================================
# UTILITIES
# ============================================================================

health: ## Проверить здоровье сервисов
	@echo "$(BLUE)▶ Проверка здоровья сервисов...$(NC)"
	./scripts/health_check.sh

generate-data: ## Сгенерировать тестовые данные
	@echo "$(BLUE)▶ Генерация данных...$(NC)"
	python scripts/generate_data.py
	@echo "$(GREEN)✓ Данные сгенерированы$(NC)"

docs-serve: ## Запустить сервер документации
	@echo "$(BLUE)▶ Запуск сервера документации...$(NC)"
	cd docs && python -m http.server 8888

install-deps: ## Установить зависимости для разработки
	@echo "$(BLUE)▶ Установка зависимостей...$(NC)"
	pip install -r requirements-dev.txt
	@echo "$(GREEN)✓ Зависимости установлены$(NC)"

# ============================================================================
# ИНФОРМАЦИЯ
# ============================================================================

info: ## Показать информацию о проекте
	@echo ""
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║                    PET PROJECT UBER                            ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(YELLOW)Сервисы:$(NC)"
	@echo "  • API Gateway      (Go)     :8080"
	@echo "  • Auth Service     (Go)     :8000"
	@echo "  • User Service     (Python) :8001"
	@echo "  • Driver Service   (Python) :8002"
	@echo "  • Ride Service     (Python) :8003"
	@echo "  • Matching Service (Go)     :8004"
	@echo "  • Geo Service      (Go)     :8005"
	@echo "  • Pricing Service  (Python) :8006"
	@echo "  • Payment Service  (Python) :8007"
	@echo "  • Notification     (Python) :8008"
	@echo "  • ML Service       (Python) :8009"
	@echo "  • AB Test Service  (Python) :8010"
	@echo "  • Analytics        (Python) :8011"
	@echo ""
	@echo "$(YELLOW)Инфраструктура:$(NC)"
	@echo "  • PostgreSQL  :5432"
	@echo "  • Redis       :6379"
	@echo "  • Kafka       :9092"
	@echo "  • Kafka UI    :9093  → http://localhost:9093"
	@echo "  • ClickHouse  :8123  → http://localhost:8123"
	@echo "  • Metabase    :3000  → http://localhost:3000"
	@echo ""
	@echo "$(YELLOW)Фронтенд:$(NC)"
	@echo "  • Passenger App  :3001  → http://localhost:3001"
	@echo "  • Driver App     :3002  → http://localhost:3002"
	@echo "  • Admin Panel    :3003  → http://localhost:3003"
	@echo ""
