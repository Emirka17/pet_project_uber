markdown
# API Documentation

## Обзор

REST API для взаимодействия с сервисами Uber-подобного приложения.

**Base URL:** `http://localhost:8080/api/v1`

**Формат:** JSON

**Аутентификация:** Bearer Token (JWT)

---

## Аутентификация

Все запросы (кроме регистрации и логина) требуют заголовок:

Authorization: Bearer <token>

bash

**Пример:**

```bash
curl -X GET http://localhost:8080/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
Коды ответов
Код	Значение	Когда
200	OK	Успешный запрос
201	Created	Ресурс создан
400	Bad Request	Неверные данные
401	Unauthorized	Нет токена или невалидный
403	Forbidden	Нет прав доступа
404	Not Found	Ресурс не найден
429	Too Many Requests	Превышен лимит запросов
500	Internal Server Error	Ошибка сервера
Формат ошибки
json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Неверный формат телефона",
    "details": {
      "field": "phone",
      "reason": "Должен начинаться с +"
    }
  }
}
Auth Service
POST /api/v1/auth/register
Регистрация нового пользователя.

Аутентификация: Не требуется

Тело запроса:

json
{
  "phone": "+12025551234",
  "name": "John Doe",
  "email": "john@example.com"
}
Поле	Тип	Обязательное	Описание
phone	string	да	Телефон в формате +XXX...
name	string	нет	Имя пользователя
email	string	нет	Email
Ответ 201:

json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "phone": "+12025551234",
    "name": "John Doe",
    "email": "john@example.com",
    "rating": 5.0,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2024-01-16T10:30:00Z"
}
Ошибки:

Код	Причина
400	Неверный формат данных
409	Телефон уже зарегистрирован
POST /api/v1/auth/login
Вход в систему.

Аутентификация: Не требуется

Тело запроса:

json
{
  "phone": "+12025551234"
}
Ответ 200:

json
{
  "message": "SMS код отправлен",
  "expires_in": 300
}
POST /api/v1/auth/verify
Подтверждение кода из SMS.

Аутентификация: Не требуется

Тело запроса:

json
{
  "phone": "+12025551234",
  "code": "123456"
}
Ответ 200:

json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "phone": "+12025551234",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2024-01-16T10:30:00Z"
}
Ошибки:

Код	Причина
400	Неверный код
410	Код истёк
POST /api/v1/auth/refresh
Обновление токена.

Аутентификация: Не требуется

Тело запроса:

json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
Ответ 200:

json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2024-01-16T10:30:00Z"
}
POST /api/v1/auth/logout
Выход из системы.

Аутентификация: Требуется

Ответ 200:

json
{
  "message": "Успешный выход"
}
User Service
GET /api/v1/users/me
Получить профиль текущего пользователя.

Аутентификация: Требуется

Ответ 200:

json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "phone": "+12025551234",
  "name": "John Doe",
  "email": "john@example.com",
  "rating": 4.85,
  "total_rides": 42,
  "created_at": "2024-01-01T00:00:00Z"
}
PATCH /api/v1/users/me
Обновить профиль.

Аутентификация: Требуется

Тело запроса:

json
{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
Ответ 200:

json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "phone": "+12025551234",
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "rating": 4.85,
  "total_rides": 42
}
GET /api/v1/users/{id}
Получить пользователя по ID (для админов).

Аутентификация: Требуется (роль: admin)

Параметры пути:

Параметр	Тип	Описание
id	UUID	ID пользователя
Ответ 200:

json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "phone": "+12025551234",
  "name": "John Doe",
  "rating": 4.85,
  "total_rides": 42,
  "created_at": "2024-01-01T00:00:00Z"
}
Driver Service
GET /api/v1/drivers/me
Получить профиль текущего водителя.

Аутентификация: Требуется (роль: driver)

Ответ 200:

json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "phone": "+12025559999",
  "name": "Иван Петров",
  "license_number": "DL123456",
  "car_model": "Toyota Camry",
  "car_plate": "ABC-1234",
  "car_color": "белый",
  "rating": 4.92,
  "total_rides": 1250,
  "is_online": true,
  "is_busy": false,
  "current_location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "created_at": "2023-06-15T00:00:00Z"
}
POST /api/v1/drivers/online
Выйти на линию.

Аутентификация: Требуется (роль: driver)

Тело запроса:

json
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
Ответ 200:

json
{
  "status": "online",
  "message": "Вы на линии"
}
POST /api/v1/drivers/offline
Уйти с линии.

Аутентификация: Требуется (роль: driver)

Ответ 200:

json
{
  "status": "offline",
  "message": "Вы не на линии",
  "summary": {
    "online_hours": 8.5,
    "rides_completed": 12,
    "earnings": 185.50
  }
}
POST /api/v1/drivers/location
Обновить координаты.

Аутентификация: Требуется (роль: driver)

Тело запроса:

json
{
  "latitude": 40.7135,
  "longitude": -74.0055
}
Ответ 200:

json
{
  "status": "updated"
}
Частота: Каждые 5-10 секунд

Ride Service
POST /api/v1/rides
Создать новую поездку.

Аутентификация: Требуется

Тело запроса:

json
{
  "pickup": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "address": "123 Main St, New York"
  },
  "dropoff": {
    "latitude": 40.7580,
    "longitude": -73.9855,
    "address": "456 Broadway, New York"
  },
  "passenger_count": 2
}
Поле	Тип	Обязательное	Описание
pickup.latitude	number	да	Широта подачи
pickup.longitude	number	да	Долгота подачи
pickup.address	string	нет	Адрес подачи
dropoff.latitude	number	да	Широта назначения
dropoff.longitude	number	да	Долгота назначения
dropoff.address	string	нет	Адрес назначения
passenger_count	integer	да	Количество пассажиров (1-9)
Ответ 201:

json
{
  "id": "ride_abc123",
  "status": "searching",
  "pickup": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "address": "123 Main St, New York"
  },
  "dropoff": {
    "latitude": 40.7580,
    "longitude": -73.9855,
    "address": "456 Broadway, New York"
  },
  "passenger_count": 2,
  "estimated_fare": {
    "min": 22.00,
    "max": 28.00,
    "currency": "USD"
  },
  "estimated_duration_minutes": 18,
  "estimated_distance_km": 7.5,
  "created_at": "2024-01-15T14:30:00Z"
}
GET /api/v1/rides/{id}
Получить информацию о поездке.

Аутентификация: Требуется

Параметры пути:

Параметр	Тип	Описание
id	string	ID поездки
Ответ 200:

json
{
  "id": "ride_abc123",
  "status": "in_progress",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe"
  },
  "driver": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Иван Петров",
    "phone": "+12025559999",
    "car_model": "Toyota Camry",
    "car_plate": "ABC-1234",
    "car_color": "белый",
    "rating": 4.92,
    "current_location": {
      "latitude": 40.7200,
      "longitude": -74.0000
    }
  },
  "pickup": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "address": "123 Main St, New York"
  },
  "dropoff": {
    "latitude": 40.7580,
    "longitude": -73.9855,
    "address": "456 Broadway, New York"
  },
  "passenger_count": 2,
  "started_at": "2024-01-15T14:35:00Z",
  "estimated_arrival": "2024-01-15T14:53:00Z",
  "created_at": "2024-01-15T14:30:00Z"
}
GET /api/v1/rides
Получить историю поездок.

Аутентификация: Требуется

Query параметры:

Параметр	Тип	По умолчанию	Описание
page	integer	1	Номер страницы
limit	integer	20	Количество на странице
status	string	all	Фильтр по статусу
Пример:

bash
GET /api/v1/rides?page=1&limit=10&status=completed
Ответ 200:

json
{
  "rides": [
    {
      "id": "ride_abc123",
      "status": "completed",
      "pickup_address": "123 Main St",
      "dropoff_address": "456 Broadway",
      "total_fare": 24.43,
      "completed_at": "2024-01-15T14:55:00Z"
    },
    {
      "id": "ride_abc122",
      "status": "completed",
      "pickup_address": "789 Park Ave",
      "dropoff_address": "321 5th Ave",
      "total_fare": 18.75,
      "completed_at": "2024-01-14T09:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 42,
    "total_pages": 5
  }
}
POST /api/v1/rides/{id}/cancel
Отменить поездку.

Аутентификация: Требуется

Параметры пути:

Параметр	Тип	Описание
id	string	ID поездки
Тело запроса:

json
{
  "reason": "Передумал"
}
Ответ 200:

json
{
  "id": "ride_abc123",
  "status": "cancelled",
  "cancellation_fee": 5.00,
  "message": "Поездка отменена"
}
Ошибки:

Код	Причина
400	Поездку нельзя отменить (уже завершена)
404	Поездка не найдена
POST /api/v1/rides/{id}/rate
Оценить поездку.

Аутентификация: Требуется

Тело запроса:

json
{
  "rating": 5,
  "comment": "Отличная поездка!"
}
Поле	Тип	Обязательное	Описание
rating	integer	да	Оценка от 1 до 5
comment	string	нет	Комментарий
Ответ 200:

json
{
  "message": "Спасибо за оценку!"
}
Pricing Service
POST /api/v1/pricing/estimate
Получить оценку стоимости поездки.

Аутентификация: Требуется

Тело запроса:

json
{
  "pickup": {
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "dropoff": {
    "latitude": 40.7580,
    "longitude": -73.9855
  }
}
Ответ 200:

json
{
  "estimates": [
    {
      "tariff": "UberX",
      "price": {
        "min": 22.00,
        "max": 28.00,
        "currency": "USD"
      },
      "duration_minutes": 18,
      "distance_km": 7.5,
      "surge_multiplier": 1.0
    },
    {
      "tariff": "UberXL",
      "price": {
        "min": 32.00,
        "max": 40.00,
        "currency": "USD"
      },
      "duration_minutes": 18,
      "distance_km": 7.5,
      "surge_multiplier": 1.0
    },
    {
      "tariff": "UberBLACK",
      "price": {
        "min": 45.00,
        "max": 55.00,
        "currency": "USD"
      },
      "duration_minutes": 18,
      "distance_km": 7.5,
      "surge_multiplier": 1.0
    }
  ]
}
GET /api/v1/pricing/tariffs
Получить список тарифов.

Аутентификация: Не требуется

Ответ 200:

json
{
  "tariffs": [
    {
      "name": "UberX",
      "description": "Экономичные поездки",
      "base_fare": 2.55,
      "per_km": 1.75,
      "per_minute": 0.35,
      "min_fare": 8.00,
      "capacity": 4
    },
    {
      "name": "UberXL",
      "description": "Для больших компаний",
      "base_fare": 3.85,
      "per_km": 2.85,
      "per_minute": 0.50,
      "min_fare": 10.00,
      "capacity": 6
    }
  ]
}
Geo Service
GET /api/v1/geo/drivers/nearby
Найти водителей рядом.

Аутентификация: Требуется

Query параметры:

Параметр	Тип	По умолчанию	Описание
latitude	number	—	Широта (обязательно)
longitude	number	—	Долгота (обязательно)
radius_km	number	3	Радиус поиска в км
limit	integer	10	Максимум результатов
Пример:

bash
GET /api/v1/geo/drivers/nearby?latitude=40.7128&longitude=-74.0060&radius_km=5
Ответ 200:

json
{
  "drivers": [
    {
      "id": "driver_1",
      "location": {
        "latitude": 40.7130,
        "longitude": -74.0055
      },
      "distance_km": 0.5,
      "eta_minutes": 2
    },
    {
      "id": "driver_2",
      "location": {
        "latitude": 40.7150,
        "longitude": -74.0080
      },
      "distance_km": 1.2,
      "eta_minutes": 4
    }
  ],
  "count": 2
}
Payment Service
GET /api/v1/payments
Получить историю платежей.

Аутентификация: Требуется

Query параметры:

Параметр	Тип	По умолчанию	Описание
page	integer	1	Номер страницы
limit	integer	20	Количество на странице
Ответ 200:

json
{
  "payments": [
    {
      "id": "pay_abc123",
      "ride_id": "ride_abc123",
      "amount": 24.43,
      "method": "card",
      "status": "completed",
      "created_at": "2024-01-15T14:55:30Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 42
  }
}
POST /api/v1/payments/methods
Добавить способ оплаты.

Аутентификация: Требуется

Тело запроса:

json
{
  "type": "card",
  "token": "tok_visa_4242"
}
Ответ 201:

json
{
  "id": "pm_abc123",
  "type": "card",
  "card": {
    "brand": "visa",
    "last4": "4242",
    "exp_month": 12,
    "exp_year": 2025
  },
  "is_default": true
}
Admin API
GET /api/v1/admin/stats
Получить статистику (для админов).

Аутентификация: Требуется (роль: admin)

Ответ 200:

json
{
  "today": {
    "rides_total": 1250,
    "rides_completed": 1180,
    "rides_cancelled": 70,
    "revenue": 28500.00,
    "active_drivers": 85,
    "active_users": 320
  },
  "week": {
    "rides_total": 8500,
    "revenue": 195000.00
  }
}
Rate Limiting
Эндпоинт	Лимит	Период
POST /auth/*	10	1 минута
POST /rides	5	1 минута
POST /drivers/location	60	1 минута
GET /*	100	1 минута
При превышении лимита — ответ 429 Too Many Requests:

json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Слишком много запросов",
    "retry_after": 45
  }
}
WebSocket API
Подключение
bash
ws://localhost:8080/ws?token=<jwt_token>
События для пассажира
json
{
  "type": "ride.driver_assigned",
  "data": {
    "ride_id": "ride_abc123",
    "driver": {
      "name": "Иван",
      "car_model": "Toyota Camry",
      "car_plate": "ABC-1234"
    },
    "eta_minutes": 5
  }
}
json
{
  "type": "ride.driver_location",
  "data": {
    "ride_id": "ride_abc123",
    "location": {
      "latitude": 40.7130,
      "longitude": -74.0055
    },
    "eta_minutes": 3
  }
}
json
{
  "type": "ride.started",
  "data": {
    "ride_id": "ride_abc123"
  }
}
json
{
  "type": "ride.completed",
  "data": {
    "ride_id": "ride_abc123",
    "fare": 24.43
  }
}
События для водителя
json
{
  "type": "ride.new_request",
  "data": {
    "ride_id": "ride_abc123",
    "pickup": {
      "address": "123 Main St",
      "distance_km": 0.8
    },
    "estimated_fare": 25.00,
    "expires_in": 15
  }
}