#!/bin/bash
# Автоматический бэкап всех баз данных

set -e  # Остановить при ошибке

BACKUP_ROOT="./backups"
DATE=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOGFILE="logs/backup_$DATE.log"

# Создать директорию для логов
mkdir -p logs

# Функция логирования
log() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a $LOGFILE
}

log "========================================="
log "Starting backup: $TIMESTAMP"
log "========================================="

# Создать директории для бэкапов
mkdir -p $BACKUP_ROOT/{postgres,redis,clickhouse}

# Счетчик ошибок
ERRORS=0

# 1. Бэкап PostgreSQL
log "Backing up PostgreSQL..."
if bash scripts/backup/backup_postgres.sh >> $LOGFILE 2>&1; then
    log "✓ PostgreSQL backup completed"
else
    log "✗ PostgreSQL backup failed"
    ERRORS=$((ERRORS + 1))
fi

# 2. Бэкап Redis
log "Backing up Redis..."
if bash scripts/backup/backup_redis.sh >> $LOGFILE 2>&1; then
    log "✓ Redis backup completed"
else
    log "✗ Redis backup failed"
    ERRORS=$((ERRORS + 1))
fi

# 3. Бэкап ClickHouse
log "Backing up ClickHouse..."
if bash scripts/backup/backup_clickhouse.sh >> $LOGFILE 2>&1; then
    log "✓ ClickHouse backup completed"
else
    log "✗ ClickHouse backup failed"
    ERRORS=$((ERRORS + 1))
fi

# 4. Очистка старых бэкапов (старше 7 дней)
log "Cleaning up old backups..."
if bash scripts/backup/cleanup_old_backups.sh >> $LOGFILE 2>&1; then
    log "✓ Cleanup completed"
else
    log "✗ Cleanup failed"
    ERRORS=$((ERRORS + 1))
fi

# 5. Показать размер бэкапов
log "Backup sizes:"
log "  PostgreSQL: $(du -sh $BACKUP_ROOT/postgres 2>/dev/null | cut -f1 || echo 'N/A')"
log "  Redis: $(du -sh $BACKUP_ROOT/redis 2>/dev/null | cut -f1 || echo 'N/A')"
log "  ClickHouse: $(du -sh $BACKUP_ROOT/clickhouse 2>/dev/null | cut -f1 || echo 'N/A')"
log "  Total: $(du -sh $BACKUP_ROOT 2>/dev/null | cut -f1 || echo 'N/A')"

# 6. Коммит в Git (опционально)
if [ "$1" == "--push-to-git" ]; then
    log "Pushing backups to GitHub..."
    cd backups
    git add . >> $LOGFILE 2>&1 || true
    git commit -m "Automated backup: $TIMESTAMP" >> $LOGFILE 2>&1 || true
    if git push origin main >> $LOGFILE 2>&1; then
        log "✓ Pushed to GitHub"
    else
        log "✗ Failed to push to GitHub"
        ERRORS=$((ERRORS + 1))
    fi
    cd ..
fi

log "========================================="
if [ $ERRORS -eq 0 ]; then
    log "Backup completed successfully: $TIMESTAMP"
    log "========================================="
    exit 0
else
    log "Backup completed with $ERRORS error(s): $TIMESTAMP"
    log "========================================="
    exit 1
fi
