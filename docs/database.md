Документация базы данных
Обзор
База данных PostgreSQL для Uber-подобного приложения. Содержит 6 таблиц.

Таблица: users
Описание: Пользователи (пассажиры) сервиса.

Поле	Тип	Обязательное	Описание
id	UUID	да	Уникальный идентификатор пользователя. Генерируется автоматически.
phone	VARCHAR(20)	да	Номер телефона. Уникальный. Формат: +1234567890
name	VARCHAR(100)	нет	Полное имя пользователя
email	VARCHAR(255)	нет	Email адрес. Уникальный.
rating	DECIMAL(3,2)	да	Рейтинг пользователя от 1.00 до 5.00. По умолчанию 5.00
total_rides	INTEGER	да	Общее количество поездок. По умолчанию 0
created_at	TIMESTAMP	да	Дата и время регистрации. По умолчанию текущее время
Первичный ключ: id

Уникальные поля: phone, email

Индексы: phone, email, rating

Таблица: drivers
Описание: Водители сервиса.

Поле	Тип	Обязательное	Описание
id	UUID	да	Уникальный идентификатор водителя. Генерируется автоматически.
phone	VARCHAR(20)	да	Номер телефона. Уникальный.
name	VARCHAR(100)	да	Полное имя водителя
email	VARCHAR(255)	нет	Email адрес. Уникальный.
license_number	VARCHAR(50)	да	Номер водительского удостоверения. Уникальный.
car_model	VARCHAR(100)	нет	Модель автомобиля. Пример: Toyota Camry
car_plate	VARCHAR(20)	нет	Номер автомобиля. Пример: ABC-1234
car_color	VARCHAR(30)	нет	Цвет автомобиля
rating	DECIMAL(3,2)	да	Рейтинг водителя от 1.00 до 5.00. По умолчанию 5.00
total_rides	INTEGER	да	Общее количество выполненных поездок. По умолчанию 0
is_online	BOOLEAN	да	Находится ли водитель на линии. По умолчанию false
is_busy	BOOLEAN	да	Занят ли водитель поездкой. По умолчанию false
current_latitude	DECIMAL(10,8)	нет	Текущая широта местоположения. Диапазон: -90 до 90
current_longitude	DECIMAL(11,8)	нет	Текущая долгота местоположения. Диапазон: -180 до 180
created_at	TIMESTAMP	да	Дата и время регистрации
Первичный ключ: id

Уникальные поля: phone, email, license_number

Индексы: phone, is_online, is_busy, (current_latitude, current_longitude)

Таблица: vendors
Описание: Справочник поставщиков услуг (компании такси).

Поле	Тип	Обязательное	Описание
id	INTEGER	да	Уникальный идентификатор поставщика. Из датасета.
name	VARCHAR(100)	да	Название компании. Пример: Uber, Lyft
description	VARCHAR(255)	нет	Описание компании
Первичный ключ: id

Начальные данные:

1 = Uber
2 = Lyft (или другой поставщик)
Таблица: rides
Описание: Поездки. Основная таблица с данными из датасета.

Поле	Тип	Обязательное	Описание
id	VARCHAR(50)	да	Уникальный идентификатор поездки. Из датасета.
user_id	UUID	нет	Идентификатор пользователя. Внешний ключ → users.id
driver_id	UUID	нет	Идентификатор водителя. Внешний ключ → drivers.id
vendor_id	INTEGER	да	Идентификатор поставщика. Внешний ключ → vendors.id
pickup_datetime	TIMESTAMP	да	Дата и время начала поездки (включение счётчика)
dropoff_datetime	TIMESTAMP	да	Дата и время окончания поездки (выключение счётчика)
passenger_count	INTEGER	да	Количество пассажиров (1-9)
pickup_latitude	DECIMAL(10,8)	да	Широта точки подачи
pickup_longitude	DECIMAL(11,8)	да	Долгота точки подачи
dropoff_latitude	DECIMAL(10,8)	да	Широта точки назначения
dropoff_longitude	DECIMAL(11,8)	да	Долгота точки назначения
pickup_district	VARCHAR(100)	нет	Район подачи. Пример: Manhattan
pickup_neighbourhood	VARCHAR(100)	нет	Квартал подачи. Пример: Upper East Side
dropoff_district	VARCHAR(100)	нет	Район назначения
dropoff_neighbourhood	VARCHAR(100)	нет	Квартал назначения
trip_duration	INTEGER	да	Длительность поездки в секундах
distance_km	DECIMAL(10,2)	нет	Расстояние поездки в километрах. Рассчитывается.
total_fare	DECIMAL(10,2)	нет	Итоговая стоимость поездки. Рассчитывается.
status	VARCHAR(20)	да	Статус поездки. По умолчанию "completed"
pickup_hour	INTEGER	нет	Час начала поездки (0-23)
day_period	VARCHAR(20)	нет	Период дня: morning, afternoon, evening, night
day_name	VARCHAR(20)	нет	День недели: Monday, Tuesday...
weekday_or_weekend	VARCHAR(10)	нет	Тип дня: weekday или weekend
regular_day_or_holiday	VARCHAR(10)	нет	Обычный день или праздник: regular или holiday
month	INTEGER	нет	Месяц (1-12)
year	INTEGER	нет	Год
season	VARCHAR(20)	нет	Сезон: spring, summer, autumn, winter
created_at	TIMESTAMP	да	Дата создания записи в БД
Первичный ключ: id

Внешние ключи:

user_id → users.id
driver_id → drivers.id
vendor_id → vendors.id
Допустимые значения status:

pending — ожидает водителя
searching — поиск водителя
assigned — водитель назначен
arriving — водитель едет
in_progress — поездка идёт
completed — завершена
cancelled — отменена
Индексы: user_id, driver_id, vendor_id, pickup_datetime, status, pickup_district, dropoff_district

Таблица: tariffs
Описание: Тарифы на поездки.

Поле	Тип	Обязательное	Описание
id	UUID	да	Уникальный идентификатор тарифа
name	VARCHAR(50)	да	Название тарифа. Уникальное. Пример: UberX, UberXL
base_fare	DECIMAL(10,2)	да	Базовая стоимость поездки в USD
per_km	DECIMAL(10,2)	да	Стоимость за километр в USD
per_minute	DECIMAL(10,2)	да	Стоимость за минуту в USD
min_fare	DECIMAL(10,2)	да	Минимальная стоимость поездки в USD
is_active	BOOLEAN	да	Активен ли тариф. По умолчанию true
created_at	TIMESTAMP	да	Дата создания
Первичный ключ: id

Уникальные поля: name

Начальные данные:

Название	Базовая	За км	За мин	Минимум
UberX	2.55	1.75	0.35	8.00
UberXL	3.85	2.85	0.50	10.00
UberBLACK	7.00	3.75	0.65	15.00
UberSUV	14.00	4.50	0.80	25.00
Таблица: payments
Описание: Платежи за поездки.

Поле	Тип	Обязательное	Описание
id	UUID	да	Уникальный идентификатор платежа
ride_id	VARCHAR(50)	да	Идентификатор поездки. Внешний ключ → rides.id
user_id	UUID	да	Идентификатор пользователя. Внешний ключ → users.id
amount	DECIMAL(10,2)	да	Сумма платежа в USD
method	VARCHAR(20)	да	Способ оплаты. По умолчанию "card"
status	VARCHAR(20)	да	Статус платежа. По умолчанию "completed"
transaction_id	VARCHAR(100)	нет	Идентификатор транзакции от платёжной системы
created_at	TIMESTAMP	да	Дата и время платежа
Первичный ключ: id

Внешние ключи:

ride_id → rides.id
user_id → users.id
Допустимые значения method:

card — банковская карта
cash — наличные
wallet — баланс в приложении
Допустимые значения status:

pending — ожидает обработки
completed — успешно
failed — ошибка
refunded — возврат
Индексы: ride_id, user_id, status

Связи между таблицами
scss
users (1) ←────────────── (N) rides
                              │
drivers (1) ←─────────────────┤
                              │
vendors (1) ←─────────────────┘

rides (1) ←────────────── (1) payments
                              │
users (1) ←───────────────────┘
Описание связей:

Один пользователь может иметь много поездок (1
)
Один водитель может выполнить много поездок (1
)
Один поставщик может иметь много поездок (1
)
Одна поездка имеет один платёж (1:1)
Один пользователь может иметь много платежей (1
)
Хранение в Redis
Ключ	Тип	TTL	Описание
session:{user_id}	STRING	24 часа	JWT токен сессии пользователя
session:{driver_id}	STRING	24 часа	JWT токен сессии водителя
driver:location:{driver_id}	HASH	—	Координаты водителя: lat, lon, updated_at
drivers
SET	—	Множество ID водителей онлайн
drivers
GEO	—	Гео-индекс для поиска ближайших водителей
rate_limit:{ip}	STRING	1 минута	Счётчик запросов для rate limiting
cache
STRING	1 час	Кэш тарифов