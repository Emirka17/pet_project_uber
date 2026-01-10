// services/matching-service/config/config.go
package config

import (
	"os"
)

type Config struct {
	KafkaBootstrapServers string
	RedisHost            string
	RedisPort            string
	PostgresHost         string
	PostgresPort         string
	PostgresDB           string
	PostgresUser         string
	PostgresPassword     string
	GroupID              string
}

func LoadConfig() Config {
	return Config{
		KafkaBootstrapServers: getEnv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092"),
		RedisHost:            getEnv("REDIS_HOST", "redis"),
		RedisPort:            getEnv("REDIS_PORT", "6379"),
		PostgresHost:         getEnv("POSTGRES_HOST", "postgres"),
		PostgresPort:         getEnv("POSTGRES_PORT", "5432"),
		PostgresDB:           getEnv("POSTGRES_DB", "uber"),
		PostgresUser:         getEnv("POSTGRES_USER", "uber"),
		PostgresPassword:     getEnv("POSTGRES_PASSWORD", "uber_secret_password"),
		GroupID:              getEnv("KAFKA_GROUP_ID", "matching-service"),
	}
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}
