// handlers/proxy.go
package handlers

import (
 "log"
 "net/http"
 "net/http/httputil"
 "net/url"
 "strings"
)

// Proxy — структура с прокси для каждого сервиса
type Proxy struct {
 UserService   *httputil.ReverseProxy
 DriverService *httputil.ReverseProxy
}

// NewProxy — создаёт новый прокси
func NewProxy(userURL, driverURL string) *Proxy {
 // Парсим URL сервисов
 userTarget, _ := url.Parse(userURL)
 driverTarget, _ := url.Parse(driverURL)

 // Создаём reverse proxy
 return &Proxy{
  UserService:   httputil.NewSingleHostReverseProxy(userTarget),
  DriverService: httputil.NewSingleHostReverseProxy(driverTarget),
 }
}

// ServeHTTP — обрабатывает входящие HTTP-запросы
func (p *Proxy) ServeHTTP(w http.ResponseWriter, r *http.Request) {
 path := r.URL.Path

 // Маршрутизация по пути
 switch {
 case strings.HasPrefix(path, "/api/v1/users"):
  log.Printf("Проксируем в User Service: %s", r.URL.Path)
  p.UserService.ServeHTTP(w, r)
 case strings.HasPrefix(path, "/api/v1/drivers"):
  log.Printf("Проксируем в Driver Service: %s", r.URL.Path)
  p.DriverService.ServeHTTP(w, r)
 default:
  http.Error(w, "Not Found", http.StatusNotFound)
 }
}
