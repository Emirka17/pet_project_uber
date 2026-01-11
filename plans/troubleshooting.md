# 🔧 Решение проблем (Troubleshooting)

## ❌ Ошибка: "blob sha256... input/output error"

### Описание проблемы
```
unable to get image 'postgres:15-alpine': Error response from daemon: 
rpc error: code = Unknown desc = blob sha256:b3968e348b48f1198cc6de6611d055dbad91cd561b7990c406c3fc28d7095b21 
expected at /var/lib/desktop-containerd/daemon/io.containerd.content.v1.content/blobs/sha256/...
open /var/lib/desktop-containerd/daemon/io.containerd.content.v1.content/blobs/sha256/...: 
input/output error
```

### Причина
Повреждение кэша Docker или проблемы с файловой системой Docker Desktop.

### Решение

#### Вариант 1: Очистка Docker кэша (Быстрое решение)

**В PowerShell или Git Bash:**

```powershell
# 1. Остановить все контейнеры
docker compose down

# 2. Очистить все неиспользуемые образы, контейнеры, сети
docker system prune -a --volumes

# Подтвердите удаление (введите 'y')
```

**Затем попробуйте снова:**
```powershell
docker compose up -d
```

#### Вариант 2: Перезапуск Docker Desktop

1. Закройте Docker Desktop полностью
2. Откройте **Диспетчер задач** (Ctrl+Shift+Esc)
3. Найдите процессы Docker и завершите их:
   - Docker Desktop
   - com.docker.backend
   - com.docker.service
4. Запустите Docker Desktop снова
5. Дождитесь полного запуска (иконка в трее станет зеленой)
6. Попробуйте снова:
```powershell
docker compose up -d
```

#### Вариант 3: Очистка данных Docker Desktop (Радикальное решение)

**⚠️ ВНИМАНИЕ: Это удалит ВСЕ образы, контейнеры и volumes!**

1. Откройте **Docker Desktop**
2. Перейдите в **Settings** (⚙️)
3. Выберите **Troubleshoot**
4. Нажмите **Clean / Purge data**
5. Подтвердите удаление
6. Перезапустите Docker Desktop
7. Попробуйте снова:
```powershell
docker compose up -d
```

#### Вариант 4: Переустановка Docker Desktop

Если ничего не помогло:

1. Удалите Docker Desktop через **Панель управления → Программы и компоненты**
2. Удалите папки:
   - `C:\Users\Администратор\.docker`
   - `C:\Users\Администратор\AppData\Local\Docker`
   - `C:\Users\Администратор\AppData\Roaming\Docker`
3. Перезагрузите компьютер
4. Скачайте и установите Docker Desktop заново: https://www.docker.com/products/docker-desktop/
5. Запустите Docker Desktop
6. Попробуйте снова:
```powershell
docker compose up -d
```

#### Вариант 5: Принудительная загрузка образов

Попробуйте загрузить образы вручную:

```powershell
# Удалить поврежденный образ
docker rmi postgres:15-alpine --force

# Загрузить заново
docker pull postgres:15-alpine

# Проверить что образ загружен
docker images | findstr postgres
```

Затем для всех остальных образов:
```powershell
docker pull redis:7-alpine
docker pull confluentinc/cp-zookeeper:7.4.0
docker pull confluentinc/cp-kafka:7.4.0
docker pull clickhouse/clickhouse-server:23.8
docker pull metabase/metabase:latest
docker pull provectuslabs/kafka-ui:latest
```

После этого:
```powershell
docker compose up -d
```

---

## ❌ Другие частые проблемы

### Проблема: Порт уже занят

**Ошибка:**
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 -> 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
```

**Решение:**

```powershell
# Найти процесс, использующий порт
netstat -ano | findstr :5432

# Убить процесс по PID (замените <PID> на реальный)
taskkill /PID <PID> /F

# Или измените порт в docker-compose.yml
# Например, для PostgreSQL:
# ports:
#   - "5433:5432"  # Вместо 5432:5432
```

### Проблема: Недостаточно памяти

**Ошибка:**
```
Error response from daemon: OCI runtime create failed
```

**Решение:**

1. Откройте **Docker Desktop**
2. **Settings** → **Resources**
3. Увеличьте:
   - **Memory**: минимум 4 GB, рекомендуется 8 GB
   - **CPUs**: минимум 2, рекомендуется 4
4. Нажмите **Apply & Restart**

### Проблема: WSL2 не установлен (Windows 10/11)

**Ошибка:**
```
Docker Desktop requires Windows Subsystem for Linux 2 (WSL2)
```

**Решение:**

```powershell
# В PowerShell от администратора
wsl --install

# Перезагрузите компьютер
# Затем установите Ubuntu из Microsoft Store
```

### Проблема: Контейнер постоянно перезапускается

**Проверка:**
```powershell
docker compose ps
# Если видите "Restarting" в статусе

# Посмотрите логи
docker compose logs [service-name]
```

**Частые причины:**
- Неправильные переменные окружения
- База данных не успела запуститься
- Ошибка в коде сервиса

**Решение:**
```powershell
# Запустите сервисы по очереди
docker compose up -d postgres redis
# Подождите 10 секунд
docker compose up -d kafka zookeeper
# Подождите 20 секунд
docker compose up -d остальные-сервисы
```

### Проблема: Kafka не запускается

**Ошибка в логах:**
```
Connection to node -1 could not be established. Broker may not be available.
```

**Решение:**

1. Убедитесь что Zookeeper запущен:
```powershell
docker compose ps zookeeper
```

2. Увеличьте время ожидания в docker-compose.yml:
```yaml
kafka:
  depends_on:
    zookeeper:
      condition: service_started
  healthcheck:
    start_period: 60s  # Увеличьте с 30s до 60s
```

3. Перезапустите:
```powershell
docker compose restart kafka
```

### Проблема: PostgreSQL не принимает подключения

**Ошибка:**
```
FATAL: password authentication failed for user "uber"
```

**Решение:**

1. Проверьте переменные окружения в `.env`:
```env
POSTGRES_USER=uber
POSTGRES_PASSWORD=uber_secret_password
POSTGRES_DB=uber
```

2. Пересоздайте контейнер:
```powershell
docker compose down postgres
docker volume rm pet_project_uber_postgres_data
docker compose up -d postgres
```

### Проблема: Redis не отвечает

**Проверка:**
```powershell
docker compose exec redis redis-cli ping
# Должно вернуть: PONG
```

**Если не отвечает:**
```powershell
docker compose restart redis
docker compose logs redis
```

---

## 🔍 Диагностика

### Проверка здоровья всех сервисов

```powershell
# Статус контейнеров
docker compose ps

# Использование ресурсов
docker stats

# Логи всех сервисов
docker compose logs --tail=50

# Логи конкретного сервиса
docker compose logs -f postgres
```

### Проверка сети

```powershell
# Список сетей
docker network ls

# Инспекция сети uber_network
docker network inspect pet_project_uber_uber_network
```

### Проверка volumes

```powershell
# Список volumes
docker volume ls

# Инспекция volume
docker volume inspect pet_project_uber_postgres_data
```

### Тест подключения к сервисам

```powershell
# PostgreSQL
docker compose exec postgres psql -U uber -d uber -c "SELECT version();"

# Redis
docker compose exec redis redis-cli ping

# Kafka
docker compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092

# ClickHouse
docker compose exec clickhouse clickhouse-client --query "SELECT version()"
```

---

## 📝 Логи и отладка

### Где искать логи

```powershell
# Все логи
docker compose logs

# Последние 100 строк
docker compose logs --tail=100

# Следить за логами в реальном времени
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f postgres

# Логи с временными метками
docker compose logs -f --timestamps
```

### Вход в контейнер для отладки

```powershell
# PostgreSQL
docker compose exec postgres bash

# Redis
docker compose exec redis sh

# Kafka
docker compose exec kafka bash

# Любой сервис
docker compose exec [service-name] sh
```

---

## 🆘 Если ничего не помогает

### Полная очистка и перезапуск

```powershell
# 1. Остановить все
docker compose down

# 2. Удалить все volumes
docker compose down -v

# 3. Удалить все образы проекта
docker images | findstr uber | ForEach-Object { docker rmi $_.Split()[2] -f }

# 4. Очистить систему Docker
docker system prune -a --volumes

# 5. Перезапустить Docker Desktop

# 6. Запустить заново
docker compose up -d
```

### Проверка системных требований

**Минимальные требования:**
- Windows 10 64-bit: Pro, Enterprise, или Education (Build 19041 или выше)
- WSL 2
- 4 GB RAM (рекомендуется 8 GB)
- 20 GB свободного места на диске

**Проверка:**
```powershell
# Версия Windows
winver

# Версия WSL
wsl --version

# Свободное место
Get-PSDrive C
```

---

## 📞 Получение помощи

Если проблема не решается:

1. **Соберите информацию:**
```powershell
docker version > docker-info.txt
docker compose version >> docker-info.txt
docker compose ps >> docker-info.txt
docker compose logs >> docker-logs.txt
```

2. **Опишите проблему:**
   - Что вы пытались сделать
   - Какую команду выполнили
   - Какую ошибку получили
   - Что уже пробовали

3. **Полезные ресурсы:**
   - Docker Documentation: https://docs.docker.com/
   - Docker Desktop Issues: https://github.com/docker/for-win/issues
   - Stack Overflow: https://stackoverflow.com/questions/tagged/docker

---

## ✅ Успешный запуск

После решения проблем, проверьте что все работает:

```powershell
# 1. Все контейнеры запущены
docker compose ps
# Все должны быть в статусе "Up"

# 2. Доступны UI
# Откройте в браузере:
# - http://localhost:9093 (Kafka UI)
# - http://localhost:3000 (Metabase)
# - http://localhost:8123 (ClickHouse)

# 3. Базы данных отвечают
docker compose exec postgres psql -U uber -d uber -c "SELECT 1;"
docker compose exec redis redis-cli ping
docker compose exec clickhouse clickhouse-client --query "SELECT 1"

# 4. Kafka работает
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

Если все проверки прошли успешно - можно продолжать разработку! 🎉
