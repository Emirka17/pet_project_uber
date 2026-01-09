#!/bin/bash
# Бэкап ClickHouse базы данных

set -e

BACKUP_DIR="./backups/clickhouse"
DATE=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/clickhouse_$DATE.tar.gz"

# Создать директорию если не существует
mkdir -p $BACKUP_DIR

echo "Creating ClickHouse backup..."

# Создать временный бэкап внутри контейнера
docker compose exec clickhouse tar czf /tmp/clickhouse_backup.tar.gz /var/lib/clickhouse/data 2>/dev/null || true

if [ $? -eq 0 ]; then
    # Скопировать бэкап из контейнера
    docker compose cp clickhouse:/tmp/clickhouse_backup.tar.gz $BACKUP_FILE
    
    # Удалить временный файл из контейнера
    docker compose exec clickhouse rm -f /tmp/clickhouse_backup.tar.gz
    
    echo "✓ ClickHouse backup created: $BACKUP_FILE"
    echo "  Size: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "✗ ClickHouse backup failed!"
    exit 1
fi
