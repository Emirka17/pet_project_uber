#!/usr/bin/env python3
"""
Скрипт загрузки датасета NYC Taxi в базу данных.

Использование:
    python scripts/generate_data.py

Что делает:
    1. Генерирует пользователей (users)
    2. Генерирует водителей (drivers)
    3. Загружает поездки из CSV (rides)
    4. Рассчитывает distance_km и total_fare
"""

import os
import sys
import uuid
import random
import math
from datetime import datetime

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from faker import Faker
from tqdm import tqdm

# Загружаем переменные из .env
load_dotenv()

# Настройки
USERS_COUNT = 10000          # Сколько пользователей сгенерировать
DRIVERS_COUNT = 5000         # Сколько водителей сгенерировать
BATCH_SIZE = 1000            # Размер пакета для вставки
DATASET_PATH = "data/nyc_taxi_trip.xlsx"

# Инициализация Faker для генерации данных
fake = Faker()


def get_db_connection():
    """Подключение к PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "uber"),
        user=os.getenv("POSTGRES_USER", "uber"),
        password=os.getenv("POSTGRES_PASSWORD", "uber_secret_password")
    )


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Рассчитать расстояние между двумя точками (формула Haversine).
    Возвращает расстояние в километрах.
    """
    R = 6371  # Радиус Земли в км
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def calculate_fare(distance_km, duration_minutes):
    """
    Рассчитать стоимость поездки.
    Базовый тариф UberX: $2.55 + $1.75/км + $0.35/мин
    """
    base_fare = 2.55
    per_km = 1.75
    per_minute = 0.35
    min_fare = 8.00
    
    fare = base_fare + (distance_km * per_km) + (duration_minutes * per_minute)
    return max(fare, min_fare)


import uuid
import random
from tqdm import tqdm
from faker import Faker

fake = Faker()

def generate_users(conn, count):
    """Генерация пользователей."""
    print(f"\n📝 Генерация {count} пользователей...")
    
    users = []
    generated_emails = set()  # Для отслеживания уникальных email
    
    for _ in tqdm(range(count)):
        while True:
            email = fake.email()
            if email not in generated_emails:
                generated_emails.add(email)
                break
        
        users.append((
            str(uuid.uuid4()),                           # id
            f"+1{fake.msisdn()[3:]}",                   # phone
            fake.name(),                                 # name
            email,                                       # email (уникальный)
            round(random.uniform(4.0, 5.0), 2),         # rating
            0,                                           # total_rides
            fake.date_time_between(start_date='-2y')    # created_at
        ))
    
    cursor = conn.cursor()
    
    # Вставляем пакетами
    for i in tqdm(range(0, len(users), BATCH_SIZE), desc="Вставка"):
        batch = users[i:i + BATCH_SIZE]
        execute_values(
            cursor,
            """
            INSERT INTO users (id, phone, name, email, rating, total_rides, created_at)
            VALUES %s
            ON CONFLICT (email) DO NOTHING
            """,  # ← Изменено с phone на email
            batch
        )
    
    conn.commit()
    cursor.close()
    
    # Получаем ID всех пользователей
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    user_ids = [str(row[0]) for row in cursor.fetchall()]
    cursor.close()
    
    print(f"✅ Создано пользователей: {len(user_ids)}")
    return user_ids


def generate_drivers(conn, count):
    """Генерация водителей."""
    print(f"\n🚗 Генерация {count} водителей...")
    
    car_models = [
        "Toyota Camry", "Honda Accord", "Ford Fusion", "Chevrolet Malibu",
        "Nissan Altima", "Hyundai Sonata", "Kia Optima", "Toyota Prius",
        "Honda Civic", "Tesla Model 3", "BMW 3 Series", "Mercedes C-Class"
    ]
    
    car_colors = ["черный", "белый", "серый", "синий", "красный", "серебристый"]
    
    drivers = []
    generated_emails = set()  # Для отслеживания уникальных email
    
    for _ in tqdm(range(count)):
        # Генерация уникального email
        while True:
            email = fake.email()
            if email not in generated_emails:
                generated_emails.add(email)
                break
        
        drivers.append((
            str(uuid.uuid4()),                           # id
            f"+1{fake.msisdn()[3:]}",                   # phone
            fake.name(),                                 # name
            email,                                       # email (уникальный)
            f"DL{fake.random_number(digits=8)}",        # license_number
            random.choice(car_models),                   # car_model
            f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}-{fake.random_number(digits=4)}",  # car_plate
            random.choice(car_colors),                   # car_color
            round(random.uniform(4.2, 5.0), 2),         # rating
            0,                                           # total_rides
            False,                                       # is_online
            False,                                       # is_busy
            None,                                        # current_latitude
            None,                                        # current_longitude
            fake.date_time_between(start_date='-2y')    # created_at
        ))
    
    cursor = conn.cursor()
    
    for i in tqdm(range(0, len(drivers), BATCH_SIZE), desc="Вставка"):
        batch = drivers[i:i + BATCH_SIZE]
        execute_values(
            cursor,
            """
            INSERT INTO drivers (
                id, phone, name, email, license_number, car_model, car_plate,
                car_color, rating, total_rides, is_online, is_busy,
                current_latitude, current_longitude, created_at
            )
            VALUES %s
            ON CONFLICT (email) DO NOTHING  
            """,# ← Изменено с phone на email
            batch
        )
    
    conn.commit()
    cursor.close()
    
    # Получаем ID всех водителей
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM drivers")
    driver_ids = [str(row[0]) for row in cursor.fetchall()]
    cursor.close()
    
    print(f"✅ Создано водителей: {len(driver_ids)}")
    return driver_ids


def load_rides(conn, user_ids, driver_ids):
    """Загрузка поездок из датасета."""
    print(f"\n📊 Загрузка поездок из {DATASET_PATH}...")
    
    # Проверяем наличие файла
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Файл не найден: {DATASET_PATH}")
        print("   Скачайте датасет и положите в папку data/")
        print("   Или выполните: python scripts/download_dataset.py")
        sys.exit(1)
    
    # Читаем файл
    print("   Чтение файла...")
    try:
        df = pd.read_excel(DATASET_PATH, engine='openpyxl')
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        print("   Попробуйте установить openpyxl: pip install openpyxl")
        sys.exit(1)
    
    print(f"   Загружено строк: {len(df)}")
    
    # Проверяем user_ids и driver_ids
    if not user_ids or not driver_ids:
        print("❌ Нет пользователей или водителей для привязки поездок!")
        return 0
    
    # Отладка: показываем первые user_id и driver_id
    print(f"   Пример user_id: {user_ids[0] if user_ids else 'Нет'}")
    print(f"   Пример driver_id: {driver_ids[0] if driver_ids else 'Нет'}")
    
    cursor = conn.cursor()
    rides_inserted = 0
    
    print("\n   Обработка и вставка поездок...")
    
    for i in tqdm(range(0, len(df), BATCH_SIZE)):
        batch_df = df.iloc[i:i + BATCH_SIZE]
        rides = []
        
        for _, row in batch_df.iterrows():
            try:
                # === ПРЕОБРАЗОВАНИЕ ТИПОВ ДАННЫХ ===
                
                # 1. ID поездки - TEXT
                ride_id = str(row.get('id', uuid.uuid4()))
                
                # 2. Случайные пользователь и водитель - TEXT (UUID строки)
                user_id = str(random.choice(user_ids))
                driver_id = str(random.choice(driver_ids))
                
                # 3. Vendor ID - INTEGER
                vendor_id = int(float(row.get('vendor_id', 1)))
                vendor_id = 1 if vendor_id not in [1, 2] else vendor_id
                
                # 4. Даты и время - TIMESTAMP
                try:
                    pickup_datetime = pd.to_datetime(row['pickup_datetime'])
                except:
                    continue  # Пропускаем некорректные даты
                
                try:
                    dropoff_datetime = pd.to_datetime(row['dropoff_datetime'])
                except:
                    # Если нет dropoff, вычисляем
                    dropoff_datetime = pickup_datetime + pd.Timedelta(minutes=random.randint(10, 60))
                
                # 5. Количество пассажиров - INTEGER
                passenger_count = int(float(row.get('passenger_count', 1)))
                passenger_count = max(1, min(9, passenger_count))
                
                # 6. Координаты - FLOAT
                try:
                    pickup_lat = float(row['pickup_latitude'])
                    pickup_lon = float(row['pickup_longitude'])
                    dropoff_lat = float(row['dropoff_latitude'])
                    dropoff_lon = float(row['dropoff_longitude'])
                except:
                    continue  # Пропускаем некорректные координаты
                
                # Проверяем валидность координат
                if not (-90 <= pickup_lat <= 90 and -180 <= pickup_lon <= 180):
                    continue
                if not (-90 <= dropoff_lat <= 90 and -180 <= dropoff_lon <= 180):
                    continue
                
                # 7. Районы - TEXT или NULL
                def safe_str(value):
                    """Преобразует значение в строку или возвращает None."""
                    if pd.isna(value):
                        return None
                    return str(value).strip() if str(value).strip() != '' else None
                
                pickup_district = safe_str(row.get('pickup_district'))
                pickup_neighbourhood = safe_str(row.get('pickup_neighbourhood'))
                dropoff_district = safe_str(row.get('dropoff_district'))
                dropoff_neighbourhood = safe_str(row.get('dropoff_neighbourhood'))
                
                # 8. Длительность поездки - INTEGER (секунды)
                trip_duration = int(float(row.get('trip_duration', 0)))
                if trip_duration <= 0:
                    # Вычисляем приблизительную длительность
                    trip_duration = random.randint(300, 3600)  # 5-60 минут
                
                # 9. Расстояние и стоимость - FLOAT
                distance_km = calculate_distance(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
                duration_minutes = trip_duration / 60
                total_fare = calculate_fare(distance_km, duration_minutes)
                
                # 10. Аналитические поля
                # pickup_hour - INTEGER (0-23)
                pickup_hour = int(pickup_datetime.hour)
                
                # day_period - TEXT или вычисляем
                day_period_raw = row.get('day_period')
                if pd.isna(day_period_raw):
                    # Вычисляем период дня по времени
                    if 5 <= pickup_hour < 12:
                        day_period = 'Morning'
                    elif 12 <= pickup_hour < 17:
                        day_period = 'Afternoon'
                    elif 17 <= pickup_hour < 22:
                        day_period = 'Evening'
                    else:
                        day_period = 'Night'
                else:
                    day_period = str(day_period_raw).strip()
                
                # day_name - TEXT
                day_name = pickup_datetime.strftime('%A')
                
                # weekday_or_weekend - TEXT
                weekday_or_weekend = 'weekend' if pickup_datetime.weekday() >= 5 else 'weekday'
                
                # regular_day_or_holiday - TEXT
                regular_day_or_holiday = 'regular'
                
                # month и year - INTEGER (не даты!)
                month = int(pickup_datetime.month)  # 1-12
                year = int(pickup_datetime.year)    # например 2023
                
                # season - TEXT или вычисляем
                season_raw = row.get('season')
                if pd.isna(season_raw):
                    # Определяем сезон по месяцу
                    if month in [12, 1, 2]:
                        season = 'Winter'
                    elif month in [3, 4, 5]:
                        season = 'Spring'
                    elif month in [6, 7, 8]:
                        season = 'Summer'
                    else:
                        season = 'Fall'
                else:
                    season = str(season_raw).strip()
                
                # 11. Статус - TEXT
                status = 'completed'
                
                # 12. created_at - TIMESTAMP
                created_at = datetime.now()
                
                # Формируем кортеж с правильными типами
                rides.append((
                    ride_id,                   # TEXT
                    user_id,                   # TEXT (UUID)
                    driver_id,                 # TEXT (UUID)
                    vendor_id,                 # INTEGER
                    pickup_datetime,           # TIMESTAMP
                    dropoff_datetime,          # TIMESTAMP
                    passenger_count,           # INTEGER
                    float(pickup_lat),         # FLOAT
                    float(pickup_lon),         # FLOAT
                    float(dropoff_lat),        # FLOAT
                    float(dropoff_lon),        # FLOAT
                    pickup_district,           # TEXT или NULL
                    pickup_neighbourhood,      # TEXT или NULL
                    dropoff_district,          # TEXT или NULL
                    dropoff_neighbourhood,     # TEXT или NULL
                    trip_duration,             # INTEGER
                    round(float(distance_km), 2),   # FLOAT (2 знака)
                    round(float(total_fare), 2),    # FLOAT (2 знака)
                    status,                    # TEXT
                    pickup_hour,               # INTEGER
                    day_period,                # TEXT
                    day_name,                  # TEXT
                    weekday_or_weekend,        # TEXT
                    regular_day_or_holiday,    # TEXT
                    month,                     # INTEGER (1-12)
                    year,                      # INTEGER
                    season,                    # TEXT
                    created_at                 # TIMESTAMP
                ))
                
            except Exception as e:
                # Пропускаем проблемные строки
                continue
        
        # Вставляем пакет
        if rides:
            try:
                execute_values(
                    cursor,
                    """
                    INSERT INTO rides (
                        id, user_id, driver_id, vendor_id,
                        pickup_datetime, dropoff_datetime, passenger_count,
                        pickup_latitude, pickup_longitude,
                        dropoff_latitude, dropoff_longitude,
                        pickup_district, pickup_neighbourhood,
                        dropoff_district, dropoff_neighbourhood,
                        trip_duration, distance_km, total_fare, status,
                        pickup_hour, day_period, day_name,
                        weekday_or_weekend, regular_day_or_holiday,
                        month, year, season, created_at
                    )
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                    """,
                    rides
                )
                conn.commit()
                rides_inserted += len(rides)
            except Exception as e:
                print(f"\n⚠️ Ошибка вставки пакета: {e}")
                # Для отладки выведем типы данных первой строки
                if rides:
                    print("Пример данных первой строки:")
                    for idx, val in enumerate(rides[0]):
                        print(f"  [{idx}] {val} (тип: {type(val).__name__})")
                conn.rollback()
    
    cursor.close()
    print(f"✅ Загружено поездок: {rides_inserted}")
    return rides_inserted


def update_ride_counts(conn):
    """Обновить счётчики поездок у пользователей и водителей."""
    print("\n📈 Обновление счётчиков поездок...")
    
    cursor = conn.cursor()
    
    # Обновляем users.total_rides
    cursor.execute("""
        UPDATE users u
        SET total_rides = (
            SELECT COUNT(*) FROM rides r WHERE r.user_id = u.id
        )
    """)
    
    # Обновляем drivers.total_rides
    cursor.execute("""
        UPDATE drivers d
        SET total_rides = (
            SELECT COUNT(*) FROM rides r WHERE r.driver_id = d.id
        )
    """)
    
    conn.commit()
    cursor.close()
    print("✅ Счётчики обновлены")


def print_stats(conn):
    """Вывести статистику по базе данных."""
    print("\n" + "="*50)
    print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ")
    print("="*50)
    
    cursor = conn.cursor()
    
    # Пользователи
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    print(f"👤 Пользователей: {users_count:,}")
    
    # Водители
    cursor.execute("SELECT COUNT(*) FROM drivers")
    drivers_count = cursor.fetchone()[0]
    print(f"🚗 Водителей: {drivers_count:,}")
    
    # Поездки
    cursor.execute("SELECT COUNT(*) FROM rides")
    rides_count = cursor.fetchone()[0]
    print(f"🛣️  Поездок: {rides_count:,}")
    
    # Статистика по поездкам
    cursor.execute("""
        SELECT 
            MIN(pickup_datetime) as first_ride,
            MAX(pickup_datetime) as last_ride,
            AVG(distance_km) as avg_distance,
            AVG(total_fare) as avg_fare,
            AVG(trip_duration) / 60 as avg_duration_min
        FROM rides
    """)
    stats = cursor.fetchone()
    
    if stats[0]:
        print(f"\n📅 Период: {stats[0].strftime('%Y-%m-%d')} — {stats[1].strftime('%Y-%m-%d')}")
        print(f"📏 Средняя дистанция: {stats[2]:.2f} км")
        print(f"💵 Средняя стоимость: ${stats[3]:.2f}")
        print(f"⏱️  Средняя длительность: {stats[4]:.1f} мин")
    
    # Топ районов
    cursor.execute("""
        SELECT pickup_district, COUNT(*) as cnt
        FROM rides
        WHERE pickup_district IS NOT NULL
        GROUP BY pickup_district
        ORDER BY cnt DESC
        LIMIT 5
    """)
    top_districts = cursor.fetchall()
    
    if top_districts:
        print(f"\n🏙️  Топ-5 районов подачи:")
        for district, count in top_districts:
            print(f"   • {district}: {count:,}")
    
    cursor.close()
    print("="*50)


def main():
    """Главная функция."""
    print("="*50)
    print("🚀 ЗАГРУЗКА ДАННЫХ В БАЗУ")
    print("="*50)
    
    # Подключаемся к БД
    print("\n🔌 Подключение к PostgreSQL...")
    try:
        conn = get_db_connection()
        print("✅ Подключено")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        sys.exit(1)
    
    try:
        # Генерируем пользователей
        user_ids = generate_users(conn, USERS_COUNT)
        
        # Генерируем водителей
        driver_ids = generate_drivers(conn, DRIVERS_COUNT)
        
        # Загружаем поездки
        load_rides(conn, user_ids, driver_ids)
        
        # Обновляем счётчики
        update_ride_counts(conn)
        
        # Выводим статистику
        print_stats(conn)
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
    
    print("\n✅ Загрузка завершена!")


if __name__ == "__main__":
    main()
