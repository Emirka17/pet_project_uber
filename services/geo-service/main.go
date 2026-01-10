// services/geo-service/main.go
package main

import (
	"log"
	"net/http"
	"geo-service/config"
	"geo-service/handlers"
	"geo-service/storage"
)

func main() {
	cfg := config.LoadConfig()

	// Создаём хранилище
	geoStorage := storage.NewGeoStorage(cfg.RedisHost, cfg.RedisPort, "")

	// Создаём обработчик
	nearbyHandler := handlers.NewNearbyHandler(geoStorage)

	// Маршрутизация
	http.Handle("/api/v1/geo/drivers/nearby", nearbyHandler)

	// Запуск сервера
	log.Printf("Geo Service запущен на порту %s", cfg.Port)
	log.Fatal(http.ListenAndServe(":"+cfg.Port, nil))
}
