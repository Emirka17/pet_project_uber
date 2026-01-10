// services/geo-service/handlers/nearby.go
package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"geo-service/storage"
)

type NearbyHandler struct {
	geoStorage *storage.GeoStorage
}

func NewNearbyHandler(geoStorage *storage.GeoStorage) *NearbyHandler {
	return &NearbyHandler{geoStorage: geoStorage}
}

func (h *NearbyHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Получаем параметры
	latStr := r.URL.Query().Get("lat")
	lonStr := r.URL.Query().Get("lon")
	radiusStr := r.URL.Query().Get("radius_km")

	if latStr == "" || lonStr == "" {
		http.Error(w, "Требуются параметры lat и lon", http.StatusBadRequest)
		return
	}

	lat, err := strconv.ParseFloat(latStr, 64)
	if err != nil {
		http.Error(w, "Неверный формат lat", http.StatusBadRequest)
		return
	}

	lon, err := strconv.ParseFloat(lonStr, 64)
	if err != nil {
		http.Error(w, "Неверный формат lon", http.StatusBadRequest)
		return
	}

	radius := 3.0 // по умолчанию 3 км
	if radiusStr != "" {
		if r, err := strconv.ParseFloat(radiusStr, 64); err == nil {
			radius = r
		}
	}

	// Ищем водителей
	drivers, err := h.geoStorage.FindNearbyDrivers(r.Context(), lat, lon, radius)
	if err != nil {
		log.Printf("Ошибка поиска: %v", err)
		http.Error(w, "Внутренняя ошибка", http.StatusInternalServerError)
		return
	}

	// Отправляем ответ
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(drivers)
}
