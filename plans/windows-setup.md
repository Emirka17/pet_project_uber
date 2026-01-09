# 🪟 Настройка проекта на Windows

## Проблема с Makefile

На Windows команда `make` не работает по умолчанию, так как это Unix-инструмент.

## Решения

### Вариант 1: Установить Make для Windows (Рекомендуется)

#### Через Chocolatey
```powershell
# Установить Chocolatey (если еще не установлен)
# Запустить PowerShell от имени администратора
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Установить Make
choco install make
```

#### Через Scoop
```powershell
# Установить Scoop
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Установить Make
scoop install make
```

#### Через Git Bash
Если у вас установлен Git for Windows, используйте **Git Bash** вместо cmd.exe:
1. Откройте Git Bash
2. Перейдите в директорию проекта: `cd /c/Users/Администратор/Desktop/pet_project_uber`
3. Запустите: `make help`

### Вариант 2: Использовать PowerShell скрипты (Альтернатива)

Я создам PowerShell скрипты, которые дублируют функциональность Makefile.

#### Использование
```powershell
# В PowerShell
.\scripts\windows\help.ps1
.\scripts\windows\up.ps1
.\scripts\windows\down.ps1
```

### Вариант 3: Использовать Docker Compose напрямую

Вместо `make` команд используйте `docker compose` напрямую:

```powershell
# Вместо: make up
docker compose up -d

# Вместо: make down
docker compose down

# Вместо: make ps
docker compose ps

# Вместо: make logs
docker compose logs -f

# Вместо: make logs-service s=user-service
docker compose logs -f user-service

# Вместо: make clean
docker compose down -v --rmi local --remove-orphans

# Вместо: make rebuild
docker compose up -d --build
```

## Основные команды для работы с проектом

### Запуск проекта
```powershell
# Запустить все сервисы
docker compose up -d

# Проверить статус
docker compose ps

# Посмотреть логи
docker compose logs -f

# Посмотреть логи конкретного сервиса
docker compose logs -f postgres
docker compose logs -f kafka
docker compose logs -f api-gateway
```

### Остановка проекта
```powershell
# Остановить сервисы
docker compose down

# Остановить и удалить volumes (БД будет очищена!)
docker compose down -v
```

### Работа с базой данных
```powershell
# Подключиться к PostgreSQL
docker compose exec postgres psql -U uber -d uber

# Подключиться к Redis
docker compose exec redis redis-cli

# Подключиться к ClickHouse
docker compose exec clickhouse clickhouse-client
```

### Работа с Kafka
```powershell
# Список топиков
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Создать топики
bash scripts/create_kafka_topics.sh

# Читать сообщения из топика
docker compose exec kafka kafka-console-consumer --topic rides.created --bootstrap-server localhost:9092 --from-beginning
```

### Миграции и данные
```powershell
# Применить миграции
bash scripts/run_migrations.sh

# Загрузить тестовые данные
python scripts/generate_data.py
```

### Тестирование
```powershell
# Unit тесты
pytest tests/ -v

# Интеграционные тесты
pytest tests/integration/ -v

# С покрытием
pytest tests/ --cov=services --cov-report=html
```

## Полезные ссылки после запуска

После выполнения `docker compose up -d` будут доступны:

- **Kafka UI**: http://localhost:9093
- **Metabase**: http://localhost:3000
- **ClickHouse**: http://localhost:8123
- **API Gateway**: http://localhost:8080
- **Passenger App**: http://localhost:3001
- **Driver App**: http://localhost:3002
- **Admin Panel**: http://localhost:3003

## Проверка работоспособности

```powershell
# Проверить что Docker запущен
docker --version
docker compose --version

# Проверить запущенные контейнеры
docker ps

# Проверить сети
docker network ls

# Проверить volumes
docker volume ls
```

## Troubleshooting

### Docker не запускается
1. Убедитесь что Docker Desktop запущен
2. Проверьте что WSL2 включен (для Windows 10/11)

### Порты заняты
```powershell
# Проверить какой процесс использует порт
netstat -ano | findstr :5432
netstat -ano | findstr :6379
netstat -ano | findstr :9092

# Убить процесс по PID
taskkill /PID <PID> /F
```

### Недостаточно памяти
В Docker Desktop:
1. Settings → Resources
2. Увеличить Memory до 4-8 GB
3. Увеличить CPU до 2-4 cores

### Ошибки при сборке
```powershell
# Очистить Docker кэш
docker system prune -a

# Пересобрать без кэша
docker compose build --no-cache
```

## Рекомендация

**Для комфортной работы на Windows рекомендую:**

1. **Установить Git Bash** (идет с Git for Windows) - это даст вам Unix-like терминал
2. **Использовать VSCode** с встроенным терминалом Git Bash
3. **Или установить Windows Terminal** + Git Bash

Тогда все команды из Makefile будут работать как на Linux/Mac!
