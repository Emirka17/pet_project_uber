#!/bin/bash
# Восстановление Redis из бэкапа

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore_redis.sh <date>"
    echo "Example: ./restore_redis.sh 20260109"
    echo ""
    echo "Available backups:"
    ls -1 backups/redis/*.rdb 2>/dev/null | sed 's/.*redis_\(.*\)\.rdb/  \1/' || echo "  No backups found"
    exit 1
fi

DATE=$1
BACKUP_FILE="./backups/redis/redis_$DATE.rdb"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "========================================="
echo "Restoring Redis from: $BACKUP_FILE"
echo "========================================="
echo ""
echo "WARNING: This will OVERWRITE current Redis data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo ""
echo "Restoring Redis..."

# Остановить Redis
echo "Stopping Redis..."
docker compose stop redis

# Скопировать RDB файл в контейнер
echo "Copying backup file..."
docker compose cp $BACKUP_FILE redis:/data/dump.rdb

# Запустить Redis
echo "Starting Redis..."
docker compose start redis

# Подождать пока Redis запустится
sleep 3

# Проверить что Redis работает
if docker compose exec redis redis-cli ping > /dev/null 2>&1; then
    echo ""
    echo "✓ Redis restored successfully"
    echo ""
    echo "Verifying restore..."
    KEYS_COUNT=$(docker compose exec redis redis-cli DBSIZE | grep -o '[0-9]*')
    echo "  Keys count: $KEYS_COUNT"
else
    echo ""
    echo "✗ Redis restore failed!"
    exit 1
fi
