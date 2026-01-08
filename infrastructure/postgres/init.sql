-- ============================================================================
-- PET PROJECT UBER — Database Schema
-- ============================================================================
-- PostgreSQL 15
-- Основано на датасете NYC Taxi Trip Duration
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Расширения
-- ----------------------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ----------------------------------------------------------------------------
-- Таблица: vendors
-- Справочник поставщиков услуг
-- ----------------------------------------------------------------------------

CREATE TABLE vendors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- Начальные данные
INSERT INTO vendors (id, name, description) VALUES
    (1, 'Uber', 'Uber Technologies Inc.'),
    (2, 'Lyft', 'Lyft Inc.');

-- ----------------------------------------------------------------------------
-- Таблица: users
-- Пользователи (пассажиры)
-- ----------------------------------------------------------------------------

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_rides INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_rating ON users(rating);

-- ----------------------------------------------------------------------------
-- Таблица: drivers
-- Водители
-- ----------------------------------------------------------------------------

CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    car_model VARCHAR(100),
    car_plate VARCHAR(20),
    car_color VARCHAR(30),
    rating DECIMAL(3,2) DEFAULT 5.00,
    total_rides INTEGER DEFAULT 0,
    is_online BOOLEAN DEFAULT FALSE,
    is_busy BOOLEAN DEFAULT FALSE,
    current_latitude DECIMAL(10,8),
    current_longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_drivers_phone ON drivers(phone);
CREATE INDEX idx_drivers_license ON drivers(license_number);
CREATE INDEX idx_drivers_status ON drivers(is_online, is_busy);
CREATE INDEX idx_drivers_location ON drivers(current_latitude, current_longitude);
CREATE INDEX idx_drivers_rating ON drivers(rating);

-- ----------------------------------------------------------------------------
-- Таблица: tariffs
-- Тарифы на поездки
-- ----------------------------------------------------------------------------

CREATE TABLE tariffs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    base_fare DECIMAL(10,2) NOT NULL,
    per_km DECIMAL(10,2) NOT NULL,
    per_minute DECIMAL(10,2) NOT NULL,
    min_fare DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Начальные данные (цены NYC 2016)
INSERT INTO tariffs (name, base_fare, per_km, per_minute, min_fare) VALUES
    ('UberX', 2.55, 1.75, 0.35, 8.00),
    ('UberXL', 3.85, 2.85, 0.50, 10.00),
    ('UberBLACK', 7.00, 3.75, 0.65, 15.00),
    ('UberSUV', 14.00, 4.50, 0.80, 25.00);

-- ----------------------------------------------------------------------------
-- Таблица: rides
-- Поездки (основная таблица, данные из датасета)
-- ----------------------------------------------------------------------------

CREATE TABLE rides (
    -- Идентификаторы
    id VARCHAR(50) PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    driver_id UUID REFERENCES drivers(id),
    vendor_id INTEGER NOT NULL REFERENCES vendors(id),
    
    -- Время
    pickup_datetime TIMESTAMP NOT NULL,
    dropoff_datetime TIMESTAMP NOT NULL,
    
    -- Пассажиры
    passenger_count INTEGER NOT NULL CHECK (passenger_count >= 1 AND passenger_count <= 9),
    
    -- Координаты подачи
    pickup_latitude DECIMAL(10,8) NOT NULL,
    pickup_longitude DECIMAL(11,8) NOT NULL,
    pickup_district VARCHAR(100),
    pickup_neighbourhood VARCHAR(100),
    
    -- Координаты назначения
    dropoff_latitude DECIMAL(10,8) NOT NULL,
    dropoff_longitude DECIMAL(11,8) NOT NULL,
    dropoff_district VARCHAR(100),
    dropoff_neighbourhood VARCHAR(100),
    
    -- Поездка
    trip_duration INTEGER NOT NULL,
    distance_km DECIMAL(10,2),
    total_fare DECIMAL(10,2),
    
    -- Статус
    status VARCHAR(20) DEFAULT 'completed',
    
    -- Аналитические поля (из датасета)
    pickup_hour INTEGER CHECK (pickup_hour >= 0 AND pickup_hour <= 23),
    day_period VARCHAR(20),
    day_name VARCHAR(20),
    weekday_or_weekend VARCHAR(10),
    regular_day_or_holiday VARCHAR(10),
    month INTEGER CHECK (month >= 1 AND month <= 12),
    year INTEGER,
    season VARCHAR(20),
    
    -- Метаданные
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы для быстрого поиска
CREATE INDEX idx_rides_user ON rides(user_id);
CREATE INDEX idx_rides_driver ON rides(driver_id);
CREATE INDEX idx_rides_vendor ON rides(vendor_id);
CREATE INDEX idx_rides_status ON rides(status);
CREATE INDEX idx_rides_pickup_datetime ON rides(pickup_datetime);
CREATE INDEX idx_rides_pickup_location ON rides(pickup_latitude, pickup_longitude);
CREATE INDEX idx_rides_dropoff_location ON rides(dropoff_latitude, dropoff_longitude);
CREATE INDEX idx_rides_pickup_district ON rides(pickup_district);
CREATE INDEX idx_rides_dropoff_district ON rides(dropoff_district);

-- Индексы для аналитики
CREATE INDEX idx_rides_pickup_hour ON rides(pickup_hour);
CREATE INDEX idx_rides_day_name ON rides(day_name);
CREATE INDEX idx_rides_month_year ON rides(year, month);
CREATE INDEX idx_rides_season ON rides(season);

-- ----------------------------------------------------------------------------
-- Таблица: payments
-- Платежи за поездки
-- ----------------------------------------------------------------------------

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ride_id VARCHAR(50) NOT NULL REFERENCES rides(id),
    user_id UUID NOT NULL REFERENCES users(id),
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(20) DEFAULT 'card',
    status VARCHAR(20) DEFAULT 'completed',
    transaction_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Ограничения
    CONSTRAINT chk_payment_method CHECK (method IN ('card', 'cash', 'wallet')),
    CONSTRAINT chk_payment_status CHECK (status IN ('pending', 'completed', 'failed', 'refunded'))
);

-- Индексы
CREATE INDEX idx_payments_ride ON payments(ride_id);
CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_created ON payments(created_at);

-- ----------------------------------------------------------------------------
-- Готово!
-- ----------------------------------------------------------------------------
