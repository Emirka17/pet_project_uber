# 🔧 Руководство по настройке системы бэкапов

## 📋 Содержание
1. [Быстрый старт](#быстрый-старт)
2. [Настройка для Linux/Mac](#настройка-для-linuxmac)
3. [Настройка для Windows](#настройка-для-windows)
4. [Автоматизация бэкапов](#автоматизация-бэкапов)
5. [Хранение в GitHub](#хранение-в-github)
6. [Тестирование](#тестирование)

---

## 🚀 Быстрый старт

### Шаг 1: Проверка структуры папок
```bash
# Должны существовать:
backups/
├── postgres/
├── redis/
└── clickhouse/
logs/
```

### Шаг 2: Первый бэкап

**Linux/Mac/Git Bash:**
```bash
chmod +x scripts/backup/*.sh scripts/restore/*.sh
./scripts/backup/backup_all.sh
```

**Windows PowerShell:**
```powershell
.\scripts\windows\backup_all.ps1
```

### Шаг 3: Проверка результата
```bash
# Проверить созданные файлы
ls -lh backups/postgres/
ls -lh backups/redis/
ls -lh backups/clickhouse/

# Проверить логи
cat logs/backup_YYYYMMDD.log
```

---

## 🐧 Настройка для Linux/Mac

### 1. Сделать скрипты исполняемыми
```bash
chmod +x scripts/backup/*.sh
chmod +x scripts/restore/*.sh
```

### 2. Проверить зависимости
```bash
# Должны быть установлены:
which docker
which docker-compose  # или docker compose
which gzip
which tar
```

### 3. Ручной запуск
```bash
# Полный бэкап всех БД
./scripts/backup/backup_all.sh

# Бэкап с отправкой в GitHub
./scripts/backup/backup_all.sh --push

# Только PostgreSQL
./scripts/backup/backup_postgres.sh

# Только Redis
./scripts/backup/backup_redis.sh

# Только ClickHouse
./scripts/backup/backup_clickhouse.sh
```

### 4. Восстановление
```bash
# Показать доступные бэкапы
./scripts/restore/restore_all.sh

# Восстановить из конкретной даты
./scripts/restore/restore_all.sh 20260109

# Восстановить только PostgreSQL
./scripts/restore/restore_postgres.sh 20260109
```

---

## 🪟 Настройка для Windows

### 1. Открыть PowerShell от администратора
```powershell
# Разрешить выполнение скриптов (один раз)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Проверить Docker
```powershell
docker --version
docker compose version
```

### 3. Ручной запуск
```powershell
# Полный бэкап
.\scripts\windows\backup_all.ps1

# Бэкап с отправкой в GitHub
.\scripts\windows\backup_all.ps1 -Push

# Восстановление
.\scripts\windows\restore_all.ps1 -Date 20260109
```

---

## ⏰ Автоматизация бэкапов

### Linux/Mac: Cron

#### 1. Открыть crontab
```bash
crontab -e
```

#### 2. Добавить задачи
```bash
# Бэкап каждый день в 3:00 ночи
0 3 * * * cd /path/to/pet_project_uber && ./scripts/backup/backup_all.sh >> logs/cron.log 2>&1

# Бэкап каждые 6 часов
0 */6 * * * cd /path/to/pet_project_uber && ./scripts/backup/backup_all.sh >> logs/cron.log 2>&1

# Очистка старых бэкапов каждую неделю
0 4 * * 0 cd /path/to/pet_project_uber && ./scripts/backup/cleanup_old_backups.sh >> logs/cleanup.log 2>&1

# Бэкап с push в GitHub каждый день в 4:00
0 4 * * * cd /path/to/pet_project_uber && ./scripts/backup/backup_all.sh --push >> logs/cron.log 2>&1
```

#### 3. Проверить задачи
```bash
crontab -l
```

### Windows: Task Scheduler

#### 1. Открыть Task Scheduler
```
Win + R → taskschd.msc
```

#### 2. Создать задачу
- **General**: Имя "Uber Backup Daily"
- **Triggers**: Daily at 3:00 AM
- **Actions**: 
  - Program: `powershell.exe`
  - Arguments: `-File "C:\path\to\pet_project_uber\scripts\windows\backup_all.ps1"`
  - Start in: `C:\path\to\pet_project_uber`

#### 3. Или через PowerShell
```powershell
# Создать задачу для ежедневного бэкапа в 3:00
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-File `"$PWD\scripts\windows\backup_all.ps1`"" `
    -WorkingDirectory $PWD

$trigger = New-ScheduledTaskTrigger -Daily -At 3am

Register-ScheduledTask -TaskName "UberBackupDaily" `
    -Action $action `
    -Trigger $trigger `
    -Description "Daily backup of Uber databases"
```

---

## 📦 Хранение в GitHub

### Вариант 1: Отдельный приватный репозиторий (рекомендуется)

#### 1. Создать репозиторий
```bash
# На GitHub создать приватный репозиторий: uber-backups
```

#### 2. Инициализировать в папке backups
```bash
cd backups
git init
git remote add origin https://github.com/YOUR_USERNAME/uber-backups.git

# Создать .gitignore
cat > .gitignore << EOF
# Игнорировать большие файлы (>100MB)
*.sql
*.rdb
*.tar.gz

# Хранить только сжатые архивы
!*.zip
!*.gz
EOF

git add .
git commit -m "Initial commit"
git push -u origin main
```

#### 3. Использовать флаг --push
```bash
# Бэкап автоматически отправится в GitHub
./scripts/backup/backup_all.sh --push
```

### Вариант 2: В основном репозитории (не рекомендуется)

```bash
# Добавить в .gitignore
echo "backups/*.sql" >> .gitignore
echo "backups/*.rdb" >> .gitignore
echo "backups/*.tar.gz" >> .gitignore
echo "!backups/**/.gitkeep" >> .gitignore

# Коммитить только структуру
git add backups/**/.gitkeep
git commit -m "Add backup structure"
```

### Вариант 3: Облачное хранилище

#### AWS S3
```bash
# Установить AWS CLI
pip install awscli

# Настроить
aws configure

# Добавить в backup_all.sh
aws s3 sync backups/ s3://your-bucket/uber-backups/
```

#### Google Drive (rclone)
```bash
# Установить rclone
curl https://rclone.org/install.sh | sudo bash

# Настроить
rclone config

# Добавить в backup_all.sh
rclone sync backups/ gdrive:uber-backups/
```

---

## 🧪 Тестирование

### 1. Тест создания бэкапа
```bash
# Запустить бэкап
./scripts/backup/backup_all.sh

# Проверить файлы
ls -lh backups/postgres/
ls -lh backups/redis/
ls -lh backups/clickhouse/

# Проверить размеры
du -sh backups/*
```

### 2. Тест восстановления
```bash
# Создать тестовые данные
docker compose exec postgres psql -U uber uber -c "INSERT INTO users (name, email, phone) VALUES ('Test User', 'test@test.com', '+79991234567');"

# Сделать бэкап
./scripts/backup/backup_all.sh

# Удалить данные
docker compose exec postgres psql -U uber uber -c "DELETE FROM users WHERE email = 'test@test.com';"

# Восстановить
./scripts/restore/restore_all.sh $(date +%Y%m%d)

# Проверить
docker compose exec postgres psql -U uber uber -c "SELECT * FROM users WHERE email = 'test@test.com';"
```

### 3. Тест автоматической очистки
```bash
# Создать старые файлы для теста
touch -t 202601010000 backups/postgres/old_backup.sql.gz

# Запустить очистку
./scripts/backup/cleanup_old_backups.sh

# Проверить что старые удалены
ls -la backups/postgres/
```

---

## 📊 Мониторинг бэкапов

### Проверка последнего бэкапа
```bash
# Linux/Mac
ls -lt backups/postgres/ | head -n 2

# Windows
Get-ChildItem backups\postgres | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### Проверка размера бэкапов
```bash
# Linux/Mac
du -sh backups/*

# Windows
Get-ChildItem backups -Recurse | Measure-Object -Property Length -Sum
```

### Проверка логов
```bash
# Последние ошибки
grep -i error logs/backup_*.log

# Статистика бэкапов
grep "Backup completed" logs/backup_*.log | wc -l
```

---

## ⚠️ Важные замечания

### 1. Безопасность
- ✅ Храните бэкапы в приватном репозитории
- ✅ Используйте шифрование для чувствительных данных
- ✅ Не коммитьте `.env` файлы с паролями
- ✅ Используйте SSH ключи для GitHub

### 2. Производительность
- ✅ Бэкапы PostgreSQL сжимаются gzip (экономия ~70%)
- ✅ Запускайте бэкапы в нерабочее время (ночью)
- ✅ Очищайте старые бэкапы (>7 дней)

### 3. Надежность
- ✅ Тестируйте восстановление регулярно
- ✅ Храните бэкапы в нескольких местах (3-2-1 правило)
- ✅ Проверяйте логи на ошибки

### 4. Ограничения GitHub
- ⚠️ Максимальный размер файла: 100 MB
- ⚠️ Рекомендуемый размер репозитория: < 1 GB
- ⚠️ Используйте Git LFS для больших файлов

---

## 🆘 Troubleshooting

### Ошибка: Permission denied
```bash
chmod +x scripts/backup/*.sh
chmod +x scripts/restore/*.sh
```

### Ошибка: Docker not found
```bash
# Проверить что Docker запущен
docker ps

# Проверить docker-compose
docker compose version
```

### Ошибка: No space left on device
```bash
# Очистить старые бэкапы
./scripts/backup/cleanup_old_backups.sh

# Очистить Docker
docker system prune -a
```

### Windows: Execution Policy Error
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Дополнительные ресурсы

- [Docker Volumes Documentation](https://docs.docker.com/storage/volumes/)
- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup.html)
- [Redis Persistence](https://redis.io/docs/management/persistence/)
- [ClickHouse Backup](https://clickhouse.com/docs/en/operations/backup)
- [Cron Tutorial](https://crontab.guru/)
- [Git LFS](https://git-lfs.github.com/)

---

## ✅ Чеклист готовности

- [ ] Структура папок создана
- [ ] Скрипты имеют права на выполнение
- [ ] Первый бэкап выполнен успешно
- [ ] Восстановление протестировано
- [ ] Настроена автоматизация (cron/Task Scheduler)
- [ ] Настроено хранение в GitHub/облаке
- [ ] Документация прочитана
- [ ] Команда знает как восстанавливать данные

---

**Готово! Ваша система бэкапов настроена и готова к использованию.** 🎉
