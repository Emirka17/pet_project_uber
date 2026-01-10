// services/matching-service/main.go
package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"matching-service/config"
	"matching-service/consumer"
	"matching-service/geo"
	"matching-service/matcher"
)

func main() {
	cfg := config.LoadConfig()

	// Создаём Kafka consumer
	kafkaConsumer := consumer.NewKafkaConsumer(
		cfg.KafkaBootstrapServers,
		cfg.GroupID,
		"rides.created",
	)

	// Создаём Geo клиент
	geoClient := geo.NewGeoClient(cfg.RedisHost, cfg.RedisPort, "")

	// Создаём Matcher
	matcher := matcher.NewMatcher(kafkaConsumer, geoClient)

	// Контекст для graceful shutdown
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Запускаем в отдельной горутине
	go func() {
		matcher.Start(ctx)
	}()

	// Ожидание сигнала завершения
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c

	log.Println("Остановка Matching Service...")
	cancel()

	// Закрываем ресурсы
	kafkaConsumer.Close()
	geoClient.Close()

	log.Println("Matching Service остановлен")
}
