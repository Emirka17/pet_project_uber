// services/matching-service/main.go
package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"
	"fmt"

	"matching-service/config"
	"matching-service/consumer"
	"matching-service/geo"
	"matching-service/matcher"
)

func main() {

   fmt.Println("1. Запуск Matching Service...")  // ← Добавь

   cfg := config.LoadConfig()

   fmt.Println("2. Конфиг загружен")  // ← Добавь

   // Создаём Kafka consumer

   kafkaConsumer := consumer.NewKafkaConsumer(

       cfg.KafkaBootstrapServers,

       cfg.GroupID,

       "rides.created",

   )

   fmt.Println("3. Kafka consumer создан")  // ← Добавь

   // Создаём Geo клиент

   geoClient := geo.NewGeoClient(cfg.RedisHost, cfg.RedisPort, "")

   fmt.Println("4. Geo клиент создан")  // ← Добавь

   // Создаём Matcher

   matcher := matcher.NewMatcher(kafkaConsumer, geoClient)

   fmt.Println("5. Matcher создан")  // ← Добавь

   // Контекст для graceful shutdown

   ctx, cancel := context.WithCancel(context.Background())

   defer cancel()

   fmt.Println("6. Запуск matcher.Start...")  // ← Добавь

   // Запускаем в отдельной горутине

   go func() {

       matcher.Start(ctx)

   }()

   fmt.Println("7. Matcher запущен")  // ← Добавь

   // Ожидание сигнала завершения

   c := make(chan os.Signal, 1)

   signal.Notify(c, os.Interrupt, syscall.SIGTERM)

   <-c

   fmt.Println("8. Получен сигнал завершения")  // ← Добавь

   log.Println("Остановка Matching Service...")

   cancel()

   // Закрываем ресурсы

   kafkaConsumer.Close()

   geoClient.Close()

   log.Println("Matching Service остановлен")

}

