// services/geo-service/config/config.go
package config

import (
	"os"
)

type Config struct {
	Port      string
	RedisHost string
	RedisPort string
}

func LoadConfig() Config {
	return Config{
		Port:      getEnv("GEO_SERVICE_PORT", "8005"),
		RedisHost: getEnv("REDIS_HOST", "redis"),
		RedisPort: getEnv("REDIS_PORT", "6379"),
	}
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}
