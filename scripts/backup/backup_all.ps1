
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
