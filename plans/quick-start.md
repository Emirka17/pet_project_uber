# 🚀 Быстрый старт - Немедленные действия

## ⚠️ Важно для Windows

На Windows команда `make` не работает в cmd.exe. У вас есть 3 варианта:

### Вариант 1: Использовать Git Bash (Рекомендуется)
1. Откройте **Git Bash** (идет с Git for Windows)
2. Перейдите в проект: `cd /c/Users/Администратор/Desktop/pet_project_uber`
3. Теперь все команды `make` будут работать!

### Вариант 2: Использовать docker compose напрямую
Вместо `make` команд используйте `docker compose`:
```powershell
# Запустить проект
docker compose up -d

# Проверить статус
docker compose ps

# Посмотреть логи
docker compose logs -f

# Остановить проект
docker compose down
```

### Вариант 3: Установить Make для Windows
```powershell
# Через Chocolatey (PowerShell от администратора)
choco install make
```

Подробнее см. [`plans/windows-setup.md`](plans/windows-setup.md)

---

## 📋 Шаг 1: Проверка окружения

### Проверьте что установлено:
```bash
# Docker
docker --version
# Должно быть: Docker version 20.x или выше

# Docker Compose
docker compose version
# Должно быть: Docker Compose version v2.x или выше

# Python (для скриптов)
python --version
# Должно быть: Python 3.9 или выше

# Go (для Go сервисов)
go version
# Должно быть: go1.20 или выше
```

### Если что-то не установлено:
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/
- **Python**: https://www.python.org/downloads/
- **Go**: https://go.dev/dl/

---

## 📋 Шаг 2: Запуск инфраструктуры

### 2.1 Запустить базовую инфраструктуру

```bash
# В Git Bash или PowerShell
docker compose up -d postgres redis kafka zookeeper clickhouse metabase kafka-ui
```

### 2.2 Проверить что все запустилось

```bash
docker compose ps
```

Должны быть запущены (status: Up):
- ✅ uber_postgres
- ✅ uber_redis
- ✅ uber_kafka
- ✅ uber_zookeeper
- ✅ uber_clickhouse
- ✅ uber_metabase
- ✅ uber_kafka_ui

### 2.3 Проверить доступность UI

Откройте в браузере:
- **Kafka UI**: http://localhost:9093 (должен открыться интерфейс)
- **Metabase**: http://localhost:3000 (первый запуск - настройка)
- **ClickHouse**: http://localhost:8123 (должен вернуть "Ok.")

---

## 📋 Шаг 3: Инициализация данных

### 3.1 Создать ClickHouse таблицы

Создайте файл [`infrastructure/clickhouse/init.sql`](infrastructure/clickhouse/init.sql):

```sql
-- Таблица событий поездок
CREATE TABLE IF NOT EXISTS analytics.ride_events (
    event_id String,
    event_type String,
    ride_id String,
    user_id String,
    driver_id String,
    timestamp DateTime,
    data String
) ENGINE = MergeTree()
ORDER BY (timestamp, ride_id);

-- Таблица дневной статистики
CREATE TABLE IF NOT EXISTS analytics.daily_stats (
    date Date,
    total_rides UInt32,
    completed_rides UInt32,
    cancelled_rides UInt32,
    total_revenue Decimal(10,2),
    avg_ride_duration Float32,
    avg_ride_distance Float32
) ENGINE = SummingMergeTree()
ORDER BY date;

-- Таблица событий водителей
CREATE TABLE IF NOT EXISTS analytics.driver_events (
    event_id String,
    event_type String,
    driver_id String,
    timestamp DateTime,
    location_lat Float64,
    location_lon Float64,
    data String
) ENGINE = MergeTree()
ORDER BY (timestamp, driver_id);
```

### 3.2 Применить миграции PostgreSQL

```bash
# Подключиться к PostgreSQL
docker compose exec postgres psql -U uber -d uber

# Проверить что таблицы созданы
\dt

# Должны быть: users, drivers, rides, payments, tariffs, ab_experiments
# Выйти: \q
```

### 3.3 Создать Kafka топики

Отредактируйте [`scripts/create_kafka_topics.sh`](scripts/create_kafka_topics.sh):

```bash
#!/bin/bash

KAFKA_CONTAINER="uber_kafka"
BOOTSTRAP_SERVER="localhost:9092"

echo "Создание Kafka топиков..."

# Топики поездок
docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic rides.created --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic rides.assigned --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic rides.started --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic rides.completed --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic rides.cancelled --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

# Топики водителей
docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic drivers.online --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic drivers.offline --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic drivers.location --partitions 6 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

# Топики платежей
docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic payments.completed --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic payments.failed --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

# Топики уведомлений
docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic notifications.push --partitions 3 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

# Топики аналитики
docker exec $KAFKA_CONTAINER kafka-topics --create --if-not-exists \
  --topic analytics.events --partitions 6 --replication-factor 1 \
  --bootstrap-server $BOOTSTRAP_SERVER

echo "✓ Топики созданы"
echo ""
echo "Список топиков:"
docker exec $KAFKA_CONTAINER kafka-topics --list --bootstrap-server $BOOTSTRAP_SERVER
```

Запустите:
```bash
# В Git Bash
bash scripts/create_kafka_topics.sh

# Или напрямую в PowerShell
docker exec uber_kafka kafka-topics --list --bootstrap-server localhost:9092
```

---

## 📋 Шаг 4: Первый микросервис - Auth Service

Это самый важный сервис, так как от него зависят все остальные.

### Что нужно реализовать в [`services/auth-service/main.go`](services/auth-service/main.go):

1. **Регистрация** - `POST /api/v1/auth/register`
2. **Логин** - `POST /api/v1/auth/login`
3. **Refresh token** - `POST /api/v1/auth/refresh`
4. **Logout** - `POST /api/v1/auth/logout`

### Технологии:
- **Gin** или **Echo** (Go web framework)
- **JWT** для токенов
- **PostgreSQL** для хранения пользователей
- **Redis** для хранения сессий

### Структура:
```
services/auth-service/
├── main.go              # Точка входа
├── config/
│   └── config.go        # Конфигурация
├── handlers/
│   ├── register.go      # POST /register
│   ├── login.go         # POST /login
│   └── refresh.go       # POST /refresh
├── jwt/
│   └── jwt.go           # Генерация и валидация JWT
└── tests/
    └── auth_test.go     # Тесты
```

### Пример минимального main.go:

```go
package main

import (
    "log"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()
    
    // Health check
    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{"status": "ok"})
    })
    
    // Auth routes
    auth := r.Group("/api/v1/auth")
    {
        auth.POST("/register", registerHandler)
        auth.POST("/login", loginHandler)
        auth.POST("/refresh", refreshHandler)
        auth.POST("/logout", logoutHandler)
    }
    
    log.Println("Auth Service starting on :8000")
    r.Run(":8000")
}

func registerHandler(c *gin.Context) {
    // TODO: Implement
    c.JSON(501, gin.H{"error": "not implemented"})
}

func loginHandler(c *gin.Context) {
    // TODO: Implement
    c.JSON(501, gin.H{"error": "not implemented"})
}

func refreshHandler(c *gin.Context) {
    // TODO: Implement
    c.JSON(501, gin.H{"error": "not implemented"})
}

func logoutHandler(c *gin.Context) {
    // TODO: Implement
    c.JSON(501, gin.H{"error": "not implemented"})
}
```

### Запуск и тестирование:

```bash
# Собрать и запустить
docker compose up -d auth-service

# Проверить логи
docker compose logs -f auth-service

# Проверить health
curl http://localhost:8000/health
```

---

## 📋 Шаг 5: API Gateway

После Auth Service реализуйте API Gateway в [`services/api-gateway/main.go`](services/api-gateway/main.go).

### Основные задачи:
1. Роутинг запросов к сервисам
2. JWT аутентификация (middleware)
3. Rate limiting через Redis
4. Логирование запросов
5. CORS

### Маршруты:
```
/api/v1/auth/*      -> auth-service:8000
/api/v1/users/*     -> user-service:8001
/api/v1/drivers/*   -> driver-service:8002
/api/v1/rides/*     -> ride-service:8003
```

---

## 📋 Шаг 6: User Service (Python)

Первый Python сервис. Реализуйте в [`services/user-service/main.py`](services/user-service/main.py).

### Технологии:
- **FastAPI**
- **SQLAlchemy** (async)
- **Pydantic** для валидации
- **Redis** для кэша

### Минимальный main.py:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="User Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/v1/users/me")
async def get_current_user():
    # TODO: Implement
    return {"error": "not implemented"}

@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: str):
    # TODO: Implement
    return {"error": "not implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Запуск:
```bash
docker compose up -d user-service
docker compose logs -f user-service
curl http://localhost:8001/health
```

---

## 📋 Приоритетный порядок разработки

### Неделя 1: Базовая инфраструктура
- [x] Запустить Docker Compose
- [ ] Создать ClickHouse init.sql
- [ ] Создать Kafka топики
- [ ] Реализовать Auth Service (Go)
- [ ] Реализовать API Gateway (Go)

### Неделя 2: CRUD сервисы
- [ ] User Service (Python)
- [ ] Driver Service (Python)
- [ ] Ride Service (Python)
- [ ] Pricing Service (Python)

### Неделя 3: Matching и Geo
- [ ] Geo Service (Go)
- [ ] Matching Service (Go)
- [ ] Интеграция через Kafka

### Неделя 4: Платежи и уведомления
- [ ] Payment Service (Python)
- [ ] Notification Service (Python)
- [ ] Analytics Service (Python)

### Неделя 5: Frontend
- [ ] Passenger App (React)
- [ ] Базовые страницы и компоненты
- [ ] Интеграция с API

---

## 🔧 Полезные команды

### Docker
```bash
# Запустить все
docker compose up -d

# Запустить только инфраструктуру
docker compose up -d postgres redis kafka zookeeper clickhouse

# Остановить все
docker compose down

# Пересобрать и запустить
docker compose up -d --build

# Посмотреть логи
docker compose logs -f [service-name]

# Очистить все (ВНИМАНИЕ: удалит данные!)
docker compose down -v
```

### База данных
```bash
# PostgreSQL
docker compose exec postgres psql -U uber -d uber

# Redis
docker compose exec redis redis-cli

# ClickHouse
docker compose exec clickhouse clickhouse-client
```

### Kafka
```bash
# Список топиков
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Читать сообщения
docker compose exec kafka kafka-console-consumer \
  --topic rides.created \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

---

## 📚 Документация

- **Полный план разработки**: [`plans/development-roadmap.md`](plans/development-roadmap.md)
- **Настройка Windows**: [`plans/windows-setup.md`](plans/windows-setup.md)
- **Архитектура**: [`docs/architecture.md`](docs/architecture.md)
- **API**: [`docs/api.md`](docs/api.md)
- **Kafka топики**: [`docs/kafka-topics.md`](docs/kafka-topics.md)
- **База данных**: [`docs/database.md`](docs/database.md)

---

## ❓ Следующие шаги

1. **Выберите способ работы с Make** (Git Bash или docker compose напрямую)
2. **Запустите инфраструктуру** (postgres, redis, kafka, clickhouse)
3. **Создайте ClickHouse init.sql** и Kafka топики
4. **Начните с Auth Service** - это фундамент всей системы
5. **Затем API Gateway** - единая точка входа
6. **Потом CRUD сервисы** - User, Driver, Ride

**Готовы начать? С чего хотите начать - с Auth Service или с настройки инфраструктуры?**
