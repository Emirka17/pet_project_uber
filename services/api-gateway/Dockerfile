# Dockerfile
FROM golang:1.21-alpine AS builder

# Рабочая папка
WORKDIR /app

# Копируем файлы
COPY . .

# Скачиваем зависимости и собираем
RUN go mod download
RUN go build -o api-gateway .

# Второй этап — минимальный образ
FROM alpine:latest

# Устанавливаем сертификаты
RUN apk --no-cache add ca-certificates

# Рабочая папка
WORKDIR /root/

# Копируем бинарник из первого этапа
COPY --from=builder /app/api-gateway .

# Открываем порт
EXPOSE 8080

# Команда запуска
CMD ["./api-gateway"]
