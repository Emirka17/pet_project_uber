#!/bin/bash
# Очистка старых бэкапов (старше 7 дней)

set -e

BACKUP_ROOT="./backups"
RETENTION_DAYS=7

echo "Cleaning up backups older than $RETENTION_DAYS days..."

# Удалить старые бэкапы PostgreSQL
if [ -d "$BACKUP_ROOT/postgres" ]; then
    DELETED=$(find $BACKUP_ROOT/postgres -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
    echo "  PostgreSQL: deleted $DELETED old backup(s)"
fi

# Удалить старые бэкапы Redis
if [ -d "$BACKUP_ROOT/redis" ]; then
    DELETED=$(find $BACKUP_ROOT/redis -name "*.rdb" -mtime +$RETENTION_DAYS -delete -print | wc -l)
    echo "  Redis: deleted $DELETED old backup(s)"
fi

# Удалить старые бэкапы ClickHouse
if [ -d "$BACKUP_ROOT/clickhouse" ]; then
    DELETED=$(find $BACKUP_ROOT/clickhouse -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete -print | wc -l)
    echo "  ClickHouse: deleted $DELETED old backup(s)"
fi

echo "✓ Old backups cleaned up"
