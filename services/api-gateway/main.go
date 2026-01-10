// main.go
package main

import (
 "log"
 "net/http"
 "api-gateway/config"
 "api-gateway/handlers"
 "api-gateway/middleware"
)

func main() {
 // Загружаем настройки
 cfg := config.LoadConfig()

 // Создаём прокси
 proxy := handlers.NewProxy(
  cfg.UserServiceURL,
  cfg.DriverServiceURL,
  cfg.RideServiceURL,
 )

 // Добавляем логирование
 handler := middleware.Logging(proxy)

 // Запускаем сервер
 log.Printf("API Gateway запущен на порту %s", cfg.Port)
 log.Fatal(http.ListenAndServe(":"+cfg.Port, handler))
}
