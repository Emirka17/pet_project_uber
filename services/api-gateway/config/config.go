// config/config.go
package config

import (
 "os"
)

// Config — структура с настройками
type Config struct {
 Port             string // Порт API Gateway
 UserServiceURL   string // URL User Service
 DriverServiceURL string // URL Driver Service
 RedisHost        string // Хост Redis
 RedisPort        string // Порт Redis
 JWTSecret        string // Секрет для JWT
}

// LoadConfig — загружает настройки из переменных окружения
func LoadConfig() Config {
 return Config{
  Port:             getEnv("API_GATEWAY_PORT", "8080"),
  UserServiceURL:   getEnv("USER_SERVICE_URL", "http://user-service:8001"),
  DriverServiceURL: getEnv("DRIVER_SERVICE_URL", "http://driver-service:8002"),
  RedisHost:        getEnv("REDIS_HOST", "redis"),
  RedisPort:        getEnv("REDIS_PORT", "6379"),
  JWTSecret:        getEnv("JWT_SECRET", "your-super-secret-jwt-key"),
 }
}

// getEnv — возвращает значение переменной окружения или значение по умолчанию
func getEnv(key, fallback string) string {
 if value, exists := os.LookupEnv(key); exists {
  return value
 }
 return fallback
}
