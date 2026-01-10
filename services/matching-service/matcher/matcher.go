// services/matching-service/matcher/matcher.go
package matcher

import (
	"context"
	"encoding/json"
	"log"
	"math/rand"

	"matching-service/consumer"
	"matching-service/geo"
)

type RideEvent struct {
	RideID    string `json:"ride_id"`
	UserID    string `json:"user_id"`
	PickupLat float64 `json:"pickup_latitude"`
	PickupLon float64 `json:"pickup_longitude"`
}

type Matcher struct {
	consumer *consumer.KafkaConsumer
	geo      *geo.GeoClient
}

func NewMatcher(consumer *consumer.KafkaConsumer, geo *geo.GeoClient) *Matcher {
	return &Matcher{
		consumer: consumer,
		geo:      geo,
	}
}

func (m *Matcher) Start(ctx context.Context) {
	handler := func(msg []byte) error {
		var event RideEvent
		if err := json.Unmarshal(msg, &event); err != nil {
			return err
		}

		log.Printf("Новая поездка: %s, pickup: %f, %f", event.RideID, event.PickupLat, event.PickupLon)

		// Ищем водителей в радиусе 3 км
		driverIDs, err := m.geo.FindNearbyDrivers(ctx, event.PickupLat, event.PickupLon, 3.0)
		if err != nil {
			return err
		}

		if len(driverIDs) == 0 {
			log.Printf("Нет водителей рядом для поездки %s", event.RideID)
			return nil
		}

		// Выбираем случайного водителя (можно улучшить: по рейтингу, расстоянию)
		selectedDriver := driverIDs[rand.Intn(len(driverIDs))]
		log.Printf("Назначен водитель %s на поездку %s", selectedDriver, event.RideID)

		// TODO: Отправить событие rides.assigned в Kafka
		// Пока просто логируем
		log.Printf("✅ Поездка %s назначена на водителя %s", event.RideID, selectedDriver)

		return nil
	}

	m.consumer.Consume(ctx, handler)
}
