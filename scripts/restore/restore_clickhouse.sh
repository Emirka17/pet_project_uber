#!/bin/bash
# Восстановление ClickHouse из бэкапа

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore_clickhouse.sh <date>"
    echo "Example: ./restore_clickhouse.sh 20260109"
    echo ""
    echo "Available backups:"
    ls -1 backups/clickhouse/*.tar.gz 2>/dev/null | sed 's/.*clickhouse_\(.*\)\.tar\.gz/  \1/' || echo "  No backups found"
    exit 1
fi

DATE=$1
BACKUP_FILE="./backups/clickhouse/clickhouse_$DATE.tar.gz"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "========================================="
echo "Restoring ClickHouse from: $BACKUP_FILE"
echo "========================================="
echo ""
echo "WARNING: This will OVERWRITE current ClickHouse data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo ""
echo "Restoring ClickHouse..."

# Скопировать бэкап в контейнер
echo "Copying backup file..."
docker compose cp $BACKUP_FILE clickhouse:/tmp/clickhouse_backup.tar.gz

# Восстановить данные
echo "Extracting backup..."
docker compose exec clickhouse sh -c "cd / && tar xzf /tmp/clickhouse_backup.tar.gz"

# Удалить временный файл
docker compose exec clickhouse rm -f /tmp/clickhouse_backup.tar.gz

# Перезапустить ClickHouse
echo "Restarting ClickHouse..."
docker compose restart clickhouse

# Подождать пока ClickHouse запустится
sleep 5

# Проверить что ClickHouse работает
if docker compose exec clickhouse clickhouse-client --query "SELECT 1" > /dev/null 2>&1; then
    echo ""
    echo "✓ ClickHouse restored successfully"
    echo ""
    echo "Verifying restore..."
    TABLES=$(docker compose exec clickhouse clickhouse-client --query "SELECT count() FROM system.tables WHERE database = 'analytics'" | tr -d ' ')
    echo "  Tables in analytics database: $TABLES"
else
    echo ""
    echo "✗ ClickHouse restore failed!"
    exit 1
fi
