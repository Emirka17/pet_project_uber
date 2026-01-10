#!/usr/bin/env python3
"""
Синхронизация онлайн водителей из PostgreSQL в Redis
"""

import psycopg2
import redis
import os
from dotenv import load_dotenv
from decimal import Decimal  # ← добавим для явного преобразования

# Загружаем переменные окружения
load_dotenv()

def main():
    # Подключение к PostgreSQL
    try:
        pg_conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", 5432),
            database=os.getenv("POSTGRES_DB", "uber"),
            user=os.getenv("POSTGRES_USER", "uber"),
            password=os.getenv("POSTGRES_PASSWORD", "uber_secret_password")
        )
        print("✅ Подключено к PostgreSQL")
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        return

    # Подключение к Redis
    try:
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True
        )
        r.ping()
        print("✅ Подключено к Redis")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        return

    try:
        cursor = pg_conn.cursor()
        
        # Получаем онлайн водителей с координатами
        cursor.execute("""
            SELECT id, current_latitude, current_longitude 
            FROM drivers 
            WHERE is_online = true 
              AND current_latitude IS NOT NULL 
              AND current_longitude IS NOT NULL
        """)
        
        drivers = cursor.fetchall()
        print(f"✅ Найдено онлайн водителей с координатами: {len(drivers)}")
        
        added = 0
        for driver_id, lat, lon in drivers:
            try:
                # 🔧 Преобразуем Decimal → float
                lat_float = float(lat) if isinstance(lat, Decimal) else lat
                lon_float = float(lon) if isinstance(lon, Decimal) else lon

                # Добавляем в GEOSET
                r.geoadd("drivers:online", [lon_float, lat_float, driver_id])
                
                # Сохраняем детали
                r.hset(f"driver:location:{driver_id}", mapping={
                    "latitude": str(lat_float),
                    "longitude": str(lon_float),
                    "updated_at": "2024-01-15T12:00:00Z"
                })
                added += 1
            except Exception as e:
                print(f"❌ Ошибка при добавлении {driver_id}: {e}")
        
        print(f"✅ Синхронизировано {added} водителей в Redis")
        
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        raise
    finally:
        cursor.close()
        pg_conn.close()

if __name__ == "__main__":
    main()
