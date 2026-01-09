# 💾 Backup & Recovery Strategy

## Обзор

Production-ready система автоматического резервного копирования для всех баз данных проекта.

**Стратегия:**
- ✅ Автоматические бэкапы каждый день в 2:00 ночи
- ✅ Хранение локально + в облаке (GitHub)
- ✅ Retention: последние 7 дней
- ✅ Бэкапы для PostgreSQL, Redis, ClickHouse
- ✅ Автоматическое восстановление одной командой

---

## Архитектура бэкапов

```
┌─────────────────────────────────────────────────────────────┐
│                    Backup System                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │    Redis     │  │  ClickHouse  │     │
│  │   Database   │  │    Cache     │  │  Analytics   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│         │ pg_dump         │ SAVE            │ clickhouse   │
│         │                 │                 │ -backup      │
│         ▼                 ▼                 ▼              │
│  ┌──────────────────────────────────────────────────┐     │
│  │         backups/ (Local Storage)                 │     │
│  │  ├── postgres_YYYYMMDD.sql.gz                    │     │
│  │  ├── redis_YYYYMMDD.rdb                          │     │
│  │  └── clickhouse_YYYYMMDD.tar.gz                  │     │
│  └──────────────────┬───────────────────────────────┘     │
│                     │                                      │
│                     │ git push                             │
│                     ▼                                      │
│  ┌──────────────────────────────────────────────────┐     │
│  │    GitHub Repository (Cloud Backup)              │     │
│  │    github.com/username/uber-backups              │     │
│  └──────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Структура файлов

```
pet_project_uber/
├── backups/                          # Локальное хранилище бэкапов
│   ├── postgres/
│   │   ├── postgres_20260109.sql.gz
│   │   ├── postgres_20260108.sql.gz
│   │   └── ...
│   ├── redis/
│   │   ├── redis_20260109.rdb
│   │   └── ...
│   ├── clickhouse/
│   │   ├── clickhouse_20260109.tar.gz
│   │   └── ...
│   └── .gitkeep
│
├── scripts/
│   ├── backup/
│   │   ├── backup_all.sh            # Главный скрипт бэкапа
│   │   ├── backup_postgres.sh       # Бэкап PostgreSQL
│   │   ├── backup_redis.sh          # Бэкап Redis
│   │   ├── backup_clickhouse.sh     # Бэкап ClickHouse
│   │   └── cleanup_old_backups.sh   # Удаление старых бэкапов
│   │
│   ├── restore/
│   │   ├── restore_all.sh           # Восстановление всех БД
│   │   ├── restore_postgres.sh      # Восстановление PostgreSQL
│   │   ├── restore_redis.sh         # Восстановление Redis
│   │   └── restore_clickhouse.sh    # Восстановление ClickHouse
│   │
│   └── windows/
│       ├── backup_all.ps1           # PowerShell версия для Windows
│       └── restore_all.ps1
│
└── docs/
    └── backup-and-recovery.md       # Этот документ
```

---

## Скрипты бэкапа

### 1. Главный скрипт: backup_all.sh

```bash
#!/bin/bash
# Автоматический бэкап всех баз данных

set -e  # Остановить при ошибке

BACKUP_ROOT="./backups"
DATE=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================="
echo "Starting backup: $TIMESTAMP"
echo "========================================="

# Создать директории
mkdir -p $BACKUP_ROOT/{postgres,redis,clickhouse}

# 1. Бэкап PostgreSQL
echo "Backing up PostgreSQL..."
bash scripts/backup/backup_postgres.sh

# 2. Бэкап Redis
echo "Backing up Redis..."
bash scripts/backup/backup_redis.sh

# 3. Бэкап ClickHouse
echo "Backing up ClickHouse..."
bash scripts/backup/backup_clickhouse.sh

# 4. Очистка старых бэкапов (старше 7 дней)
echo "Cleaning up old backups..."
bash scripts/backup/cleanup_old_backups.sh

# 5. Коммит в Git (опционально)
if [ "$1" == "--push-to-git" ]; then
    echo "Pushing backups to GitHub..."
    git add backups/
    git commit -m "Automated backup: $TIMESTAMP" || true
    git push origin main || echo "Warning: Failed to push to GitHub"
fi

echo "========================================="
echo "Backup completed: $TIMESTAMP"
echo "========================================="
```

### 2. Бэкап PostgreSQL: backup_postgres.sh

```bash
#!/bin/bash

BACKUP_DIR="./backups/postgres"
DATE=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/postgres_$DATE.sql"

echo "Creating PostgreSQL backup..."

# Создать бэкап
docker compose exec -T postgres pg_dump -U uber uber > $BACKUP_FILE

# Сжать
gzip -f $BACKUP_FILE

echo "✓ PostgreSQL backup created: $BACKUP_FILE.gz"
echo "  Size: $(du -h $BACKUP_FILE.gz | cut -f1)"
```

### 3. Бэкап Redis: backup_redis.sh

```bash
#!/bin/bash

BACKUP_DIR="./backups/redis"
DATE=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/redis_$DATE.rdb"

echo "Creating Redis backup..."

# Сохранить данные Redis на диск
docker compose exec redis redis-cli SAVE

# Скопировать RDB файл из контейнера
docker compose cp redis:/data/dump.rdb $BACKUP_FILE

echo "✓ Redis backup created: $BACKUP_FILE"
echo "  Size: $(du -h $BACKUP_FILE | cut -f1)"
```

### 4. Бэкап ClickHouse: backup_clickhouse.sh

```bash
#!/bin/bash

BACKUP_DIR="./backups/clickhouse"
DATE=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/clickhouse_$DATE.tar.gz"

echo "Creating ClickHouse backup..."

# Создать бэкап через clickhouse-backup (если установлен)
# Или просто скопировать данные
docker compose exec clickhouse clickhouse-client --query "BACKUP DATABASE analytics TO Disk('backups', 'backup_$DATE')" || {
    # Fallback: копировать директорию данных
    docker compose exec clickhouse tar czf /tmp/backup.tar.gz /var/lib/clickhouse/data/analytics
    docker compose cp clickhouse:/tmp/backup.tar.gz $BACKUP_FILE
}

echo "✓ ClickHouse backup created: $BACKUP_FILE"
echo "  Size: $(du -h $BACKUP_FILE | cut -f1)"
```

### 5. Очистка старых бэкапов: cleanup_old_backups.sh

```bash
#!/bin/bash

BACKUP_ROOT="./backups"
RETENTION_DAYS=7

echo "Cleaning up backups older than $RETENTION_DAYS days..."

# Удалить старые бэкапы PostgreSQL
find $BACKUP_ROOT/postgres -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Удалить старые бэкапы Redis
find $BACKUP_ROOT/redis -name "*.rdb" -mtime +$RETENTION_DAYS -delete

# Удалить старые бэкапы ClickHouse
find $BACKUP_ROOT/clickhouse -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "✓ Old backups cleaned up"
```

---

## Скрипты восстановления

### 1. Главный скрипт: restore_all.sh

```bash
#!/bin/bash
# Восстановление всех баз данных из бэкапа

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore_all.sh <date>"
    echo "Example: ./restore_all.sh 20260109"
    echo ""
    echo "Available backups:"
    ls -1 backups/postgres/*.sql.gz | sed 's/.*postgres_\(.*\)\.sql\.gz/  \1/'
    exit 1
fi

DATE=$1

echo "========================================="
echo "Restoring from backup: $DATE"
echo "========================================="
echo ""
echo "WARNING: This will OVERWRITE current data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# 1. Восстановить PostgreSQL
echo "Restoring PostgreSQL..."
bash scripts/restore/restore_postgres.sh $DATE

# 2. Восстановить Redis
echo "Restoring Redis..."
bash scripts/restore/restore_redis.sh $DATE

# 3. Восстановить ClickHouse
echo "Restoring ClickHouse..."
bash scripts/restore/restore_clickhouse.sh $DATE

echo "========================================="
echo "Restore completed: $DATE"
echo "========================================="
```

### 2. Восстановление PostgreSQL: restore_postgres.sh

```bash
#!/bin/bash

DATE=$1
BACKUP_FILE="./backups/postgres/postgres_$DATE.sql.gz"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring PostgreSQL from: $BACKUP_FILE"

# Распаковать и восстановить
gunzip -c $BACKUP_FILE | docker compose exec -T postgres psql -U uber uber

echo "✓ PostgreSQL restored"
```

### 3. Восстановление Redis: restore_redis.sh

```bash
#!/bin/bash

DATE=$1
BACKUP_FILE="./backups/redis/redis_$DATE.rdb"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring Redis from: $BACKUP_FILE"

# Остановить Redis
docker compose stop redis

# Скопировать RDB файл в контейнер
docker compose cp $BACKUP_FILE redis:/data/dump.rdb

# Запустить Redis
docker compose start redis

echo "✓ Redis restored"
```

### 4. Восстановление ClickHouse: restore_clickhouse.sh

```bash
#!/bin/bash

DATE=$1
BACKUP_FILE="./backups/clickhouse/clickhouse_$DATE.tar.gz"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring ClickHouse from: $BACKUP_FILE"

# Скопировать бэкап в контейнер
docker compose cp $BACKUP_FILE clickhouse:/tmp/backup.tar.gz

# Восстановить
docker compose exec clickhouse sh -c "cd /var/lib/clickhouse/data && tar xzf /tmp/backup.tar.gz"

# Перезапустить ClickHouse
docker compose restart clickhouse

echo "✓ ClickHouse restored"
```

---

## PowerShell версия для Windows

### backup_all.ps1

```powershell
# Автоматический бэкап всех баз данных (Windows)

$BackupRoot = ".\backups"
$Date = Get-Date -Format "yyyyMMdd"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "=========================================" -ForegroundColor Blue
Write-Host "Starting backup: $Timestamp" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

# Создать директории
New-Item -ItemType Directory -Force -Path "$BackupRoot\postgres" | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupRoot\redis" | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupRoot\clickhouse" | Out-Null

# 1. Бэкап PostgreSQL
Write-Host "Backing up PostgreSQL..." -ForegroundColor Yellow
$pgBackup = "$BackupRoot\postgres\postgres_$Date.sql"
docker compose exec -T postgres pg_dump -U uber uber > $pgBackup
Compress-Archive -Path $pgBackup -DestinationPath "$pgBackup.zip" -Force
Remove-Item $pgBackup
Write-Host "✓ PostgreSQL backup created" -ForegroundColor Green

# 2. Бэкап Redis
Write-Host "Backing up Redis..." -ForegroundColor Yellow
docker compose exec redis redis-cli SAVE | Out-Null
docker compose cp redis:/data/dump.rdb "$BackupRoot\redis\redis_$Date.rdb"
Write-Host "✓ Redis backup created" -ForegroundColor Green

# 3. Бэкап ClickHouse
Write-Host "Backing up ClickHouse..." -ForegroundColor Yellow
docker compose exec clickhouse tar czf /tmp/backup.tar.gz /var/lib/clickhouse/data/analytics
docker compose cp clickhouse:/tmp/backup.tar.gz "$BackupRoot\clickhouse\clickhouse_$Date.tar.gz"
Write-Host "✓ ClickHouse backup created" -ForegroundColor Green

# 4. Очистка старых бэкапов (старше 7 дней)
Write-Host "Cleaning up old backups..." -ForegroundColor Yellow
$RetentionDate = (Get-Date).AddDays(-7)
Get-ChildItem -Path "$BackupRoot\postgres" -Filter "*.zip" | Where-Object { $_.LastWriteTime -lt $RetentionDate } | Remove-Item
Get-ChildItem -Path "$BackupRoot\redis" -Filter "*.rdb" | Where-Object { $_.LastWriteTime -lt $RetentionDate } | Remove-Item
Get-ChildItem -Path "$BackupRoot\clickhouse" -Filter "*.tar.gz" | Where-Object { $_.LastWriteTime -lt $RetentionDate } | Remove-Item
Write-Host "✓ Old backups cleaned up" -ForegroundColor Green

Write-Host "=========================================" -ForegroundColor Blue
Write-Host "Backup completed: $Timestamp" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue
```

---

## Настройка автоматического запуска

### Linux/Mac (Cron)

```bash
# Открыть crontab
crontab -e

# Добавить строку (бэкап каждый день в 2:00)
0 2 * * * cd /path/to/pet_project_uber && bash scripts/backup/backup_all.sh --push-to-git >> logs/backup.log 2>&1
```

### Windows (Планировщик заданий)

1. Открой **Планировщик заданий** (Task Scheduler)
2. **Создать задачу** → **Общие**:
   - Имя: `Uber Backup Daily`
   - Выполнять независимо от входа пользователя
3. **Триггеры** → **Создать**:
   - Ежедневно в 2:00
4. **Действия** → **Создать**:
   - Программа: `powershell.exe`
   - Аргументы: `-File C:\Users\Администратор\Desktop\pet_project_uber\scripts\windows\backup_all.ps1`
   - Рабочая папка: `C:\Users\Администратор\Desktop\pet_project_uber`
5. **Условия**:
   - Снять галочку "Запускать только при питании от сети"
6. **Параметры**:
   - Разрешить выполнение задачи по требованию

---

## Хранение в облаке (GitHub)

### Настройка отдельного репозитория для бэкапов

```bash
# 1. Создать новый репозиторий на GitHub
# Название: uber-backups (приватный!)

# 2. Инициализировать Git в папке backups
cd backups
git init
git add .
git commit -m "Initial backup"

# 3. Подключить к GitHub
git remote add origin https://github.com/username/uber-backups.git
git branch -M main
git push -u origin main

# 4. Настроить .gitignore
echo "*.log" > .gitignore
git add .gitignore
git commit -m "Add gitignore"
git push
```

### Автоматическая загрузка бэкапов

Добавь в конец `backup_all.sh`:

```bash
# Загрузить в GitHub
cd backups
git add .
git commit -m "Automated backup: $(date +%Y%m%d_%H%M%S)"
git push origin main
cd ..
```

### Альтернатива: Git LFS для больших файлов

```bash
# Установить Git LFS
git lfs install

# Отслеживать большие файлы
git lfs track "*.sql.gz"
git lfs track "*.tar.gz"
git lfs track "*.rdb"

git add .gitattributes
git commit -m "Add Git LFS tracking"
git push
```

---

## Мониторинг бэкапов

### Проверка успешности бэкапа

Создай `scripts/backup/verify_backup.sh`:

```bash
#!/bin/bash

DATE=$(date +%Y%m%d)

echo "Verifying backups for $DATE..."

# Проверить PostgreSQL
if [ -f "backups/postgres/postgres_$DATE.sql.gz" ]; then
    SIZE=$(du -h "backups/postgres/postgres_$DATE.sql.gz" | cut -f1)
    echo "✓ PostgreSQL backup exists ($SIZE)"
else
    echo "✗ PostgreSQL backup missing!"
    exit 1
fi

# Проверить Redis
if [ -f "backups/redis/redis_$DATE.rdb" ]; then
    SIZE=$(du -h "backups/redis/redis_$DATE.rdb" | cut -f1)
    echo "✓ Redis backup exists ($SIZE)"
else
    echo "✗ Redis backup missing!"
    exit 1
fi

# Проверить ClickHouse
if [ -f "backups/clickhouse/clickhouse_$DATE.tar.gz" ]; then
    SIZE=$(du -h "backups/clickhouse/clickhouse_$DATE.tar.gz" | cut -f1)
    echo "✓ ClickHouse backup exists ($SIZE)"
else
    echo "✗ ClickHouse backup missing!"
    exit 1
fi

echo "All backups verified successfully!"
```

### Уведомления при ошибках

Добавь в `backup_all.sh`:

```bash
# В начале скрипта
LOGFILE="logs/backup_$(date +%Y%m%d).log"
mkdir -p logs

# Перенаправить вывод в лог
exec > >(tee -a $LOGFILE)
exec 2>&1

# В конце скрипта
if [ $? -eq 0 ]; then
    echo "SUCCESS: Backup completed" | mail -s "Backup Success" admin@example.com
else
    echo "ERROR: Backup failed" | mail -s "Backup Failed" admin@example.com
fi
```

---

## Тестирование восстановления

### Регулярный тест восстановления

Создай `scripts/test/test_restore.sh`:

```bash
#!/bin/bash

echo "Testing backup restore process..."

# 1. Создать тестовую БД
docker compose exec postgres psql -U uber -c "CREATE DATABASE uber_test;"

# 2. Восстановить последний бэкап в тестовую БД
LATEST_BACKUP=$(ls -t backups/postgres/*.sql.gz | head -1)
gunzip -c $LATEST_BACKUP | docker compose exec -T postgres psql -U uber uber_test

# 3. Проверить количество записей
RIDES_COUNT=$(docker compose exec postgres psql -U uber uber_test -t -c "SELECT COUNT(*) FROM rides;")
echo "Restored rides count: $RIDES_COUNT"

# 4. Удалить тестовую БД
docker compose exec postgres psql -U uber -c "DROP DATABASE uber_test;"

echo "✓ Restore test completed successfully"
```

Запускай этот тест раз в неделю чтобы убедиться что бэкапы рабочие!

---

## Метрики для резюме

### Что показать на собеседовании

1. **Автоматизация:**
   - Скрипты для всех БД
   - Автоматический запуск по расписанию
   - Автоматическая очистка старых бэкапов

2. **Надежность:**
   - Локальное + облачное хранение
   - Retention policy (7 дней)
   - Проверка успешности бэкапов

3. **Восстановление:**
   - Скрипты восстановления одной командой
   - Тестирование восстановления
   - Документация процесса

4. **Мониторинг:**
   - Логирование всех операций
   - Уведомления при ошибках
   - Метрики размера бэкапов

### Вопросы на собеседовании

**Q: Как часто делаете бэкапы?**
A: Автоматически каждый день в 2:00 ночи. Храним последние 7 дней локально и в GitHub.

**Q: Как быстро можете восстановить систему?**
A: Одной командой `./restore_all.sh 20260109`. Полное восстановление занимает ~5-10 минут.

**Q: Что если GitHub недоступен?**
A: Локальные бэкапы всегда доступны. GitHub - это дополнительная защита.

**Q: Как тестируете бэкапы?**
A: Раз в неделю запускаем тест восстановления в отдельную БД и проверяем данные.

**Q: Что в production?**
A: В production использовал бы AWS RDS с автоматическими бэкапами, point-in-time recovery, и Multi-AZ deployment.

---

## Команды для использования

### Создание бэкапа

```bash
# Все БД
bash scripts/backup/backup_all.sh

# С загрузкой в GitHub
bash scripts/backup/backup_all.sh --push-to-git

# Только PostgreSQL
bash scripts/backup/backup_postgres.sh

# Windows
.\scripts\windows\backup_all.ps1
```

### Восстановление

```bash
# Посмотреть доступные бэкапы
ls -1 backups/postgres/*.sql.gz

# Восстановить все БД
bash scripts/restore/restore_all.sh 20260109

# Только PostgreSQL
bash scripts/restore/restore_postgres.sh 20260109
```

### Проверка

```bash
# Проверить бэкапы
bash scripts/backup/verify_backup.sh

# Тест восстановления
bash scripts/test/test_restore.sh

# Размер бэкапов
du -sh backups/*
```

---

## Итого

✅ **Реализовано:**
- Автоматические бэкапы всех БД (PostgreSQL, Redis, ClickHouse)
- Ежедневное расписание (2:00 ночи)
- Локальное + облачное хранение (GitHub)
- Retention: 7 дней
- Скрипты восстановления
- Мониторинг и проверка
- Документация

✅ **Для резюме:**
- Production-ready решение
- Автоматизация
- Disaster Recovery Plan
- Понимание best practices
