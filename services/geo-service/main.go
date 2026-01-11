// services/geo-service/main.go
package main

import (
	"log"
	"encoding/json"
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

	// mux := http.NewServerMux()

	// Добавь health check
  	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
    	w.Header().Set("Content-Type", "application/json")
    	json.NewEncoder(w).Encode(map[string]string{"status": "healthy", "service": "geo-service"})
  	})

	http.HandleFunc("/api/v1/geo/health", func(w http.ResponseWriter, r *http.Request) {
    	w.Header().Set("Content-Type", "application/json")
    	json.NewEncoder(w).Encode(map[string]string{"status": "healthy", "service": "geo-service", "endpoint": "api/v1/geo"})
  	})

	// Маршрутизация
	http.HandleFunc("/api/v1/geo/drivers/nearby", func(w http.ResponseWriter, r *http.Request) {
		nearbyHandler.ServeHTTP(w,r)
	})

	// Запуск сервера
	log.Printf("Geo Service запущен на порту %s", cfg.Port)
	log.Fatal(http.ListenAndServe(":"+cfg.Port, nil))

}
