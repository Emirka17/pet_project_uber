// handlers/proxy.go
package handlers

import (

"log"

"net/http"

"net/http/httputil"

"net/url"

"strings"

)

type Proxy struct {
	UserService   *httputil.ReverseProxy
	DriverService *httputil.ReverseProxy
	RideService   *httputil.ReverseProxy
	GeoService    *httputil.ReverseProxy
	PricingService    *httputil.ReverseProxy
	PaymentService    *httputil.ReverseProxy
	NotificationService    *httputil.ReverseProxy  


}

// NewProxy — создаёт новый прокси

func NewProxy(userURL, driverURL, rideURL, geoURL, notificationURL, paymentURL, pricingURL string) *Proxy {

// Парсим URL сервисов
	userTarget, _ := url.Parse(userURL)
	driverTarget, _ := url.Parse(driverURL)
	rideTarget, _ := url.Parse(rideURL)
	geoTarget, _ := url.Parse(geoURL)
	notificationTarget, _ := url.Parse(notificationURL)
	paymentTarget, _ := url.Parse(paymentURL)
	pricingTarget, _ := url.Parse(pricingURL)

	return &Proxy{

	UserService:   httputil.NewSingleHostReverseProxy(userTarget),
	DriverService: httputil.NewSingleHostReverseProxy(driverTarget),
	RideService:   httputil.NewSingleHostReverseProxy(rideTarget),
	GeoService:    httputil.NewSingleHostReverseProxy(geoTarget), 
	PricingService:   httputil.NewSingleHostReverseProxy(pricingTarget),
	PaymentService:    httputil.NewSingleHostReverseProxy(paymentTarget),
	NotificationService:    httputil.NewSingleHostReverseProxy(notificationTarget), 

	}

}

func (p *Proxy) ServeHTTP(w http.ResponseWriter, r *http.Request) {
path := r.URL.Path
switch {

case strings.HasPrefix(path, "/api/v1/users"):
 log.Printf("Проксируем в User Service: %s", r.URL.Path)
 p.UserService.ServeHTTP(w, r)
case strings.HasPrefix(path, "/api/v1/drivers"):
 log.Printf("Проксируем в Driver Service: %s", r.URL.Path)
 p.DriverService.ServeHTTP(w, r)
case strings.HasPrefix(path, "/api/v1/rides"):
 log.Printf("Проксируем в Ride Service: %s", r.URL.Path)
 p.RideService.ServeHTTP(w, r)
case strings.HasPrefix(path, "/api/v1/notifications"):
 log.Printf("Проксируем в Notification Service: %s", r.URL.Path)
 p.NotificationService.ServeHTTP(w, r)
case strings.HasPrefix(path, "/api/v1/payments"):
 log.Printf("Проксируем в Payment Service: %s", r.URL.Path)
 r.URL.Path = path
 p.PaymentService.ServeHTTP(w, r)
case strings.HasPrefix(path, "/api/v1/pricing"):
 log.Printf("Проксируем в Pricing Service: %s", r.URL.Path)
 p.PricingService.ServeHTTP(w, r)
case strings.HasPrefix(path, "/api/v1/geo"):
 log.Printf("Проксируем в Geo Service: %s", r.URL.Path)
 p.GeoService.ServeHTTP(w, r)
default:
 http.Error(w, "Not Found", http.StatusNotFound)

}

}

