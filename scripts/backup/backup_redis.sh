#!/bin/bash
# Бэкап Redis базы данных

set -e

BACKUP_DIR="./backups/redis"
DATE=$(date +%Y%m%d)
BACKUP_FILE="$BACKUP_DIR/redis_$DATE.rdb"

# Создать директорию если не существует
mkdir -p $BACKUP_DIR

echo "Creating Redis backup..."

# Сохранить данные Redis на диск
docker compose exec redis redis-cli SAVE > /dev/null 2>&1

if [ $? -eq 0 ]; then
    # Скопировать RDB файл из контейнера
    docker compose cp redis:/data/dump.rdb $BACKUP_FILE
    
    echo "✓ Redis backup created: $BACKUP_FILE"
    echo "  Size: $(du -h $BACKUP_FILE | cut -f1)"
else
    echo "✗ Redis backup failed!"
    exit 1
fi
