# Автоматический бэкап всех баз данных (Windows PowerShell)

$ErrorActionPreference = "Stop"

$BackupRoot = ".\backups"
$Date = Get-Date -Format "yyyyMMdd"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = "logs\backup_$Date.log"

# Создать директорию для логов
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Функция логирования
function Write-Log {
    param($Message)
    $LogMessage = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
    Write-Host $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage
}

Write-Log "========================================="
Write-Log "Starting backup: $Timestamp"
Write-Log "========================================="

# Создать директории для бэкапов
New-Item -ItemType Directory -Force -Path "$BackupRoot\postgres" | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupRoot\redis" | Out-Null
New-Item -ItemType Directory -Force -Path "$BackupRoot\clickhouse" | Out-Null

# Счетчик ошибок
$Errors = 0

# 1. Бэкап PostgreSQL
Write-Log "Backing up PostgreSQL..."
try {
    $pgBackup = "$BackupRoot\postgres\postgres_$Date.sql"
    docker compose exec -T postgres pg_dump -U uber uber > $pgBackup
    
    if ($LASTEXITCODE -eq 0) {
        Compress-Archive -Path $pgBackup -DestinationPath "$pgBackup.zip" -Force
        Remove-Item $pgBackup
        $Size = (Get-Item "$pgBackup.zip").Length / 1MB
        Write-Log "✓ PostgreSQL backup created: $pgBackup.zip ($([math]::Round($Size, 2)) MB)"
    } else {
        throw "pg_dump failed"
    }
} catch {
    Write-Log "✗ PostgreSQL backup failed: $_"
    $Errors++
}

# 2. Бэкап Redis
Write-Log "Backing up Redis..."
try {
    docker compose exec redis redis-cli SAVE | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        docker compose cp redis:/data/dump.rdb "$BackupRoot\redis\redis_$Date.rdb"
        $Size = (Get-Item "$BackupRoot\redis\redis_$Date.rdb").Length / 1MB
        Write-Log "✓ Redis backup created: $BackupRoot\redis\redis_$Date.rdb ($([math]::Round($Size, 2)) MB)"
    } else {
        throw "Redis SAVE failed"
    }
} catch {
    Write-Log "✗ Redis backup failed: $_"
    $Errors++
}

# 3. Бэкап ClickHouse
Write-Log "Backing up ClickHouse..."
try {
    docker compose exec clickhouse tar czf /tmp/clickhouse_backup.tar.gz /var/lib/clickhouse/data 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        docker compose cp clickhouse:/tmp/clickhouse_backup.tar.gz "$BackupRoot\clickhouse\clickhouse_$Date.tar.gz"
        docker compose exec clickhouse rm -f /tmp/clickhouse_backup.tar.gz
        $Size = (Get-Item "$BackupRoot\clickhouse\clickhouse_$Date.tar.gz").Length / 1MB
        Write-Log "✓ ClickHouse backup created: $BackupRoot\clickhouse\clickhouse_$Date.tar.gz ($([math]::Round($Size, 2)) MB)"
    } else {
        throw "ClickHouse backup failed"
    }
} catch {
    Write-Log "✗ ClickHouse backup failed: $_"
    $Errors++
}

# 4. Очистка старых бэкапов (старше 7 дней)
Write-Log "Cleaning up old backups..."
try {
    $RetentionDate = (Get-Date).AddDays(-7)
    
    $DeletedPG = (Get-ChildItem -Path "$BackupRoot\postgres" -Filter "*.zip" -ErrorAction SilentlyContinue | 
        Where-Object { $_.LastWriteTime -lt $RetentionDate } | 
        Remove-Item -PassThru).Count
    
    $DeletedRedis = (Get-ChildItem -Path "$BackupRoot\redis" -Filter "*.rdb" -ErrorAction SilentlyContinue | 
        Where-Object { $_.LastWriteTime -lt $RetentionDate } | 
        Remove-Item -PassThru).Count
    
    $DeletedCH = (Get-ChildItem -Path "$BackupRoot\clickhouse" -Filter "*.tar.gz" -ErrorAction SilentlyContinue | 
        Where-Object { $_.LastWriteTime -lt $RetentionDate } | 
        Remove-Item -PassThru).Count
    
    Write-Log "  PostgreSQL: deleted $DeletedPG old backup(s)"
    Write-Log "  Redis: deleted $DeletedRedis old backup(s)"
    Write-Log "  ClickHouse: deleted $DeletedCH old backup(s)"
    Write-Log "✓ Cleanup completed"
} catch {
    Write-Log "✗ Cleanup failed: $_"
    $Errors++
}

# 5. Показать размер бэкапов
Write-Log "Backup sizes:"
try {
    $PGSize = (Get-ChildItem -Path "$BackupRoot\postgres" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    $RedisSize = (Get-ChildItem -Path "$BackupRoot\redis" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    $CHSize = (Get-ChildItem -Path "$BackupRoot\clickhouse" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    $TotalSize = $PGSize + $RedisSize + $CHSize
    
    Write-Log "  PostgreSQL: $([math]::Round($PGSize, 2)) MB"
    Write-Log "  Redis: $([math]::Round($RedisSize, 2)) MB"
    Write-Log "  ClickHouse: $([math]::Round($CHSize, 2)) MB"
    Write-Log "  Total: $([math]::Round($TotalSize, 2)) MB"
} catch {
    Write-Log "  Could not calculate sizes"
}

Write-Log "========================================="
if ($Errors -eq 0) {
    Write-Log "Backup completed successfully: $Timestamp"
    Write-Log "========================================="
    exit 0
} else {
    Write-Log "Backup completed with $Errors error(s): $Timestamp"
    Write-Log "========================================="
    exit 1
}
