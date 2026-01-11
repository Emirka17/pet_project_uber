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
 RideServiceURL   string // URL Ride Service
 NotificationServiceURL    string // URL Notification Service
 PaymentServiceURL    string // URL Payment Service
 PricingServiceURL    string // URL Pricing Service
 GeoServiceURL    string // URL Geo Service
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
  RideServiceURL:   getEnv("RIDE_SERVICE_URL", "http://ride-service:8003"),
  NotificationServiceURL:    getEnv("NOTIFICATION_SERVICE_URL", "http://notification-service:8008"),
  PaymentServiceURL:    getEnv("PAYMENT_SERVICE_URL", "http://payment-service:8007"),
  PricingServiceURL:    getEnv("PRICING_SERVICE_URL", "http://pricing-service:8006"),
  GeoServiceURL:    getEnv("GEO_SERVICE_URL", "http://geo-service:8005"),
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
