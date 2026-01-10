// services/geo-service/storage/redis_geo.go
package storage

import (
	"context"
	"fmt"
	"log"

	"github.com/go-redis/redis/v8"
)

type GeoStorage struct {
	client *redis.Client
}

func NewGeoStorage(host, port, password string) *GeoStorage {
	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", host, port),
		Password: password,
		DB:       0,
	})

	return &GeoStorage{client: client}
}

type DriverLocation struct {
	DriverID string  `json:"driver_id"`
	Lat      float64 `json:"lat"`
	Lon      float64 `json:"lon"`
	Distance float64 `json:"distance_km"`
}

func (g *GeoStorage) FindNearbyDrivers(ctx context.Context, lat, lon, radius float64) ([]DriverLocation, error) {
	locations, err := g.client.GeoRadius(ctx, "drivers:online", lon, lat, &redis.GeoRadiusQuery{
		Radius:     radius,
		Unit:       "km",
		WithDist:   true,
		WithCoord:  true,
		Sort:       "ASC",
	}).Result()

	if err != nil {
		return nil, err
	}

	var drivers []DriverLocation
	for _, loc := range locations {
		distance := loc.Dist / 1000 // meters to km
		driver := DriverLocation{
			DriverID: loc.Name,
			Lat:      loc.GeoPos.Lat,
			Lon:      loc.GeoPos.Long,
			Distance: distance,
		}
		drivers = append(drivers, driver)
	}

	log.Printf("Найдено водителей: %d в радиусе %.1f км", len(drivers), radius)
	return drivers, nil
}
