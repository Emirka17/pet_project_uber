# Восстановление всех баз данных из бэкапа (Windows PowerShell)

param(
    [Parameter(Mandatory=$false)]
    [string]$Date
)

$ErrorActionPreference = "Stop"

# Если дата не указана, показать доступные бэкапы
if (-not $Date) {
    Write-Host "Usage: .\restore_all.ps1 -Date <YYYYMMDD>" -ForegroundColor Yellow
    Write-Host "Example: .\restore_all.ps1 -Date 20260109" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available backups:" -ForegroundColor Cyan
    
    $Backups = Get-ChildItem -Path "backups\postgres" -Filter "*.zip" -ErrorAction SilentlyContinue |
        ForEach-Object { $_.Name -replace 'postgres_(\d{8})\.sql\.zip', '$1' } |
        Sort-Object -Descending
    
    if ($Backups) {
        $Backups | ForEach-Object { Write-Host "  $_" -ForegroundColor Green }
    } else {
        Write-Host "  No backups found" -ForegroundColor Red
    }
    exit 1
}

Write-Host "=========================================" -ForegroundColor Blue
Write-Host "Restoring ALL databases from backup: $Date" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "This will restore:" -ForegroundColor Yellow
Write-Host "  - PostgreSQL"
Write-Host "  - Redis"
Write-Host "  - ClickHouse"
Write-Host ""
Write-Host "WARNING: This will OVERWRITE ALL current data!" -ForegroundColor Red
$Confirm = Read-Host "Are you sure? (yes/no)"

if ($Confirm -ne "yes") {
    Write-Host "Restore cancelled" -ForegroundColor Yellow
    exit 0
}

$Errors = 0

# 1. Восстановить PostgreSQL
Write-Host ""
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "1/3: Restoring PostgreSQL..." -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

$PGBackup = "backups\postgres\postgres_$Date.sql.zip"
if (-not (Test-Path $PGBackup)) {
    Write-Host "✗ Error: Backup file not found: $PGBackup" -ForegroundColor Red
    $Errors++
} else {
    try {
        # Распаковать
        $TempSQL = "backups\postgres\temp_restore.sql"
        Expand-Archive -Path $PGBackup -DestinationPath "backups\postgres" -Force
        Move-Item "backups\postgres\postgres_$Date.sql" $TempSQL -Force
        
        # Восстановить
        Get-Content $TempSQL | docker compose exec -T postgres psql -U uber uber
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ PostgreSQL restored successfully" -ForegroundColor Green
            
            # Проверка
            $RidesCount = docker compose exec -T postgres psql -U uber uber -t -c "SELECT COUNT(*) FROM rides;"
            $UsersCount = docker compose exec -T postgres psql -U uber uber -t -c "SELECT COUNT(*) FROM users;"
            Write-Host "  Rides: $($RidesCount.Trim())" -ForegroundColor Cyan
            Write-Host "  Users: $($UsersCount.Trim())" -ForegroundColor Cyan
        } else {
            throw "psql restore failed"
        }
        
        # Удалить временный файл
        Remove-Item $TempSQL -ErrorAction SilentlyContinue
    } catch {
        Write-Host "✗ PostgreSQL restore failed: $_" -ForegroundColor Red
        $Errors++
    }
}

# 2. Восстановить Redis
Write-Host ""
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "2/3: Restoring Redis..." -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

$RedisBackup = "backups\redis\redis_$Date.rdb"
if (-not (Test-Path $RedisBackup)) {
    Write-Host "✗ Error: Backup file not found: $RedisBackup" -ForegroundColor Red
    $Errors++
} else {
    try {
        # Остановить Redis
        Write-Host "Stopping Redis..." -ForegroundColor Yellow
        docker compose stop redis
        
        # Скопировать RDB файл
        Write-Host "Copying backup file..." -ForegroundColor Yellow
        docker compose cp $RedisBackup redis:/data/dump.rdb
        
        # Запустить Redis
        Write-Host "Starting Redis..." -ForegroundColor Yellow
        docker compose start redis
        
        # Подождать
        Start-Sleep -Seconds 3
        
        # Проверить
        $Ping = docker compose exec redis redis-cli ping 2>$null
        if ($Ping -match "PONG") {
            Write-Host "✓ Redis restored successfully" -ForegroundColor Green
            
            $KeysCount = docker compose exec redis redis-cli DBSIZE
            Write-Host "  Keys count: $KeysCount" -ForegroundColor Cyan
        } else {
            throw "Redis not responding"
        }
    } catch {
        Write-Host "✗ Redis restore failed: $_" -ForegroundColor Red
        $Errors++
    }
}

# 3. Восстановить ClickHouse
Write-Host ""
Write-Host "=========================================" -ForegroundColor Blue
Write-Host "3/3: Restoring ClickHouse..." -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue

$CHBackup = "backups\clickhouse\clickhouse_$Date.tar.gz"
if (-not (Test-Path $CHBackup)) {
    Write-Host "✗ Error: Backup file not found: $CHBackup" -ForegroundColor Red
    $Errors++
} else {
    try {
        # Скопировать бэкап в контейнер
        Write-Host "Copying backup file..." -ForegroundColor Yellow
        docker compose cp $CHBackup clickhouse:/tmp/clickhouse_backup.tar.gz
        
        # Восстановить
        Write-Host "Extracting backup..." -ForegroundColor Yellow
        docker compose exec clickhouse sh -c "cd / && tar xzf /tmp/clickhouse_backup.tar.gz"
        
        # Удалить временный файл
        docker compose exec clickhouse rm -f /tmp/clickhouse_backup.tar.gz
        
        # Перезапустить
        Write-Host "Restarting ClickHouse..." -ForegroundColor Yellow
        docker compose restart clickhouse
        
        # Подождать
        Start-Sleep -Seconds 5
        
        # Проверить
        $Test = docker compose exec clickhouse clickhouse-client --query "SELECT 1" 2>$null
        if ($Test -match "1") {
            Write-Host "✓ ClickHouse restored successfully" -ForegroundColor Green
        } else {
            throw "ClickHouse not responding"
        }
    } catch {
        Write-Host "✗ ClickHouse restore failed: $_" -ForegroundColor Red
        $Errors++
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Blue
if ($Errors -eq 0) {
    Write-Host "All databases restored successfully!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Blue
    exit 0
} else {
    Write-Host "Restore completed with $Errors error(s)" -ForegroundColor Red
    Write-Host "=========================================" -ForegroundColor Blue
    exit 1
}
