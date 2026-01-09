#!/bin/bash
# Восстановление всех баз данных из бэкапа

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore_all.sh <date>"
    echo "Example: ./restore_all.sh 20260109"
    echo ""
    echo "Available backups:"
    ls -1 backups/postgres/*.sql.gz 2>/dev/null | sed 's/.*postgres_\(.*\)\.sql\.gz/  \1/' || echo "  No backups found"
    exit 1
fi

DATE=$1

echo "========================================="
echo "Restoring ALL databases from backup: $DATE"
echo "========================================="
echo ""
echo "This will restore:"
echo "  - PostgreSQL"
echo "  - Redis"
echo "  - ClickHouse"
echo ""
echo "WARNING: This will OVERWRITE ALL current data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

ERRORS=0

# 1. Восстановить PostgreSQL
echo ""
echo "========================================="
echo "1/3: Restoring PostgreSQL..."
echo "========================================="
if bash scripts/restore/restore_postgres.sh $DATE; then
    echo "✓ PostgreSQL restored"
else
    echo "✗ PostgreSQL restore failed"
    ERRORS=$((ERRORS + 1))
fi

# 2. Восстановить Redis
echo ""
echo "========================================="
echo "2/3: Restoring Redis..."
echo "========================================="
if bash scripts/restore/restore_redis.sh $DATE; then
    echo "✓ Redis restored"
else
    echo "✗ Redis restore failed"
    ERRORS=$((ERRORS + 1))
fi

# 3. Восстановить ClickHouse
echo ""
echo "========================================="
echo "3/3: Restoring ClickHouse..."
echo "========================================="
if bash scripts/restore/restore_clickhouse.sh $DATE; then
    echo "✓ ClickHouse restored"
else
    echo "✗ ClickHouse restore failed"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "========================================="
if [ $ERRORS -eq 0 ]; then
    echo "All databases restored successfully!"
    echo "========================================="
    exit 0
else
    echo "Restore completed with $ERRORS error(s)"
    echo "========================================="
    exit 1
fi
