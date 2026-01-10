// services/matching-service/geo/redis_geo.go
package geo

import (
	"context"
	"fmt"
	"log"

	"github.com/go-redis/redis/v8"
)

type GeoClient struct {
	client *redis.Client
}

func NewGeoClient(host, port, password string) *GeoClient {
	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", host, port),
		Password: password,
		DB:       0,
 	})

 	return &GeoClient{client: client}
}

func (g *GeoClient) FindNearbyDrivers(ctx context.Context, lat, lon float64, radius float64) ([]string, error) {
	// Для go-redis v8 используем GeoRadiusQuery
	locations, err := g.client.GeoRadius(ctx, "drivers:online", lon, lat, &redis.GeoRadiusQuery{
		Radius:     radius,
		Unit:       "km",
		WithDist:   true,
		WithGeoHash: false,
		WithCoord: true,  // ← Правильное имя
		Count:      0,
		Sort:       "ASC",
	}).Result()

	if err != nil {
	return nil, err
 	}

	var driverIDs []string
	for _, loc := range locations {
	driverIDs = append(driverIDs, loc.Name)
	}

	log.Printf("Найдено водителей рядом: %d", len(driverIDs))
	return driverIDs, nil
}

func (g *GeoClient) Close() error {
	return g.client.Close()
}
