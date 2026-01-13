#  Uber Clone - Pet Project

Микросервисное приложение для заказа такси, вдохновленное архитектурой Uber.

##  **Обзор**

Full-stack приложение с event-driven архитектурой, включающее:
- **7 backend микросервисов** на Go и Python
- **React frontend** с полным UX флоу
- **Docker Compose** инфраструктура
- **Kafka** для асинхронной коммуникации

## 🏗️ **Архитектура**

┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Frontend │ │ API Gateway │ │ Services │
│ (React) │───▶│ (Go) │───▶│ (Go/Python) │
│ │ │ │ │ │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│
┌───────┼───────┐
▼ ▼ ▼
┌─────────┐┌─────────┐┌─────────┐
│ Kafka ││PostgreSQL││ Redis │
│ ││ ││ │
└─────────┘└─────────┘└─────────┘


##  **Реализованные сервисы**

### **Backend (7/13):**
- ✅ **User Service** - управление пассажирами
- ✅ **Driver Service** - управление водителями
- ✅ **Ride Service** - создание поездок
- ✅ **Geo Service** - поиск водителей рядом
- ✅ **Pricing Service** - расчет стоимости
- ✅ **Payment Service** - обработка платежей
- ✅ **Notification Service** - уведомления

### **Frontend:**
- ✅ **Passenger App** - интерфейс пассажира
- Полный флоу: регистрация → заказ → отслеживание → оплата

## 🛠️ **Технологии**

### **Backend:**
- Go (API Gateway, Matching, Geo)
- Python (FastAPI - остальные сервисы)
- PostgreSQL, Redis, ClickHouse
- Apache Kafka

### **Frontend:**
- React + Tailwind CSS
- React Router
- Leaflet Maps

### **Инфраструктура:**
- Docker + Docker Compose
- Nginx (в планах)

## 📱 **Функционал**

### **Пассажир:**
- Регистрация/авторизация
- Заказ поездки с выбором на карте
- Отслеживание водителя в real-time
- Расчет стоимости поездки
- История поездок
- Оплата поездки

### **Event-driven flow:**
1. Создание поездки → Kafka (`rides.created`)
2. Поиск водителя → Kafka (`rides.assigned`)
3. Обработка платежа → Kafka (`payments.processed`)
4. Уведомления → Kafka (`notifications.send`)

##  **Быстрый старт**

```bash
# Клонирование
git clone <repo-url>
cd pet_project_uber

# Запуск backend
docker-compose up -d

# Запуск frontend
cd frontend/passenger-app
npm install
npm start
