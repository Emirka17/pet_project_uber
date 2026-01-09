#!/bin/bash
# Восстановление PostgreSQL из бэкапа

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore_postgres.sh <date>"
    echo "Example: ./restore_postgres.sh 20260109"
    echo ""
    echo "Available backups:"
    ls -1 backups/postgres/*.sql.gz 2>/dev/null | sed 's/.*postgres_\(.*\)\.sql\.gz/  \1/' || echo "  No backups found"
    exit 1
fi

DATE=$1
BACKUP_FILE="./backups/postgres/postgres_$DATE.sql.gz"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "========================================="
echo "Restoring PostgreSQL from: $BACKUP_FILE"
echo "========================================="
echo ""
echo "WARNING: This will OVERWRITE current PostgreSQL data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo ""
echo "Restoring PostgreSQL..."

# Распаковать и восстановить
gunzip -c $BACKUP_FILE | docker compose exec -T postgres psql -U uber uber

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ PostgreSQL restored successfully"
    echo ""
    echo "Verifying restore..."
    RIDES_COUNT=$(docker compose exec -T postgres psql -U uber uber -t -c "SELECT COUNT(*) FROM rides;" | tr -d ' ')
    USERS_COUNT=$(docker compose exec -T postgres psql -U uber uber -t -c "SELECT COUNT(*) FROM users;" | tr -d ' ')
    DRIVERS_COUNT=$(docker compose exec -T postgres psql -U uber uber -t -c "SELECT COUNT(*) FROM drivers;" | tr -d ' ')
    
    echo "  Rides: $RIDES_COUNT"
    echo "  Users: $USERS_COUNT"
    echo "  Drivers: $DRIVERS_COUNT"
else
    echo ""
    echo "✗ PostgreSQL restore failed!"
    exit 1
fi
