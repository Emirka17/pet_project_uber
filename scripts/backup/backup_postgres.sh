#!/bin/bash
# Простой бэкап PostgreSQL

BACKUP_DIR="./backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/postgres_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

echo "Creating PostgreSQL backup..."

# Одна команда: дамп + сжатие
docker compose exec -T postgres bash -c 'PGPASSWORD=uber_secret_password pg_dump -U uber uber' | gzip > "$BACKUP_FILE"

if [ -s "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✓ Backup created: $BACKUP_FILE ($SIZE)"
else
    echo "✗ Backup failed!"
    exit 1
fi
