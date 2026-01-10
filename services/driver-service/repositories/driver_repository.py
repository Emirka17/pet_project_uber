# services/driver-service/repositories/driver_repository.py
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from models.driver import Driver, DriverCreate, DriverUpdate
import redis
import os


class DriverRepository:
    def __init__(self, connection):
        self.conn = connection
        # Подключение к Redis
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True
        )
    
    def get_driver(self, driver_id: str) -> Optional[Driver]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM drivers WHERE id = %s", 
                (driver_id,)
            )
            row = cur.fetchone()
            if row:
                return Driver(**row)
        return None
    
    def get_driver_by_phone(self, phone: str) -> Optional[Driver]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM drivers WHERE phone = %s", 
                (phone,)
            )
            row = cur.fetchone()
            if row:
                return Driver(**row)
        return None
    
    def get_drivers(self, skip: int = 0, limit: int = 100) -> List[Driver]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM drivers ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, skip)
            )
            rows = cur.fetchall()
            return [Driver(**row) for row in rows]
    
        def create_driver(self, driver: DriverCreate) -> Driver:
        driver_id = str(uuid.uuid4())
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO drivers (
                    id, phone, name, email, license_number, car_model, car_plate,
                    car_color, rating, total_rides, is_online, is_busy,
                    current_latitude, current_longitude, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING *
                """,
                (
                    driver_id, driver.phone, driver.name, driver.email,
                    driver.license_number, driver.car_model, driver.car_plate,
                    driver.car_color, driver.rating, driver.total_rides,
                    driver.is_online, driver.is_busy, driver.current_latitude,
                    driver.current_longitude
                )
            )
            row = cur.fetchone()
            self.conn.commit()
            
            # 🔁 Синхронизация с Redis
            if driver.is_online and driver.current_latitude and driver.current_longitude:
                self.add_driver_to_redis(driver_id, driver.current_latitude, driver.current_longitude)
            
            return Driver(**row)

    
        def update_driver(self, driver_id: str, driver: DriverUpdate) -> Optional[Driver]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE drivers 
                SET name = %s, email = %s, car_model = %s, car_plate = %s,
                    car_color = %s, rating = %s, is_online = %s, is_busy = %s,
                    current_latitude = %s, current_longitude = %s
                WHERE id = %s
                RETURNING *
                """,
                (
                    driver.name, driver.email, driver.car_model, driver.car_plate,
                    driver.car_color, driver.rating, driver.is_online, driver.is_busy,
                    driver.current_latitude, driver.current_longitude, driver_id
                )
            )
            row = cur.fetchone()
            if row:
                self.conn.commit()
                
                # 🔁 Синхронизация с Redis
                if driver.is_online and driver.current_latitude and driver.current_longitude:
                    self.add_driver_to_redis(driver_id, driver.current_latitude, driver.current_longitude)
                else:
                    self.remove_driver_from_redis(driver_id)
                
                return Driver(**row)
            return None

    
    def delete_driver(self, driver_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM drivers WHERE id = %s",
                (driver_id,)
            )
            self.conn.commit()
            return cur.rowcount > 0
        def add_driver_to_redis(self, driver_id: str, lat: float, lon: float):
        """Добавить водителя в Redis при is_online = true"""
        try:
            # Добавляем в GEOSET
            self.redis_client.geoadd("drivers:online", [lon, lat, driver_id])
            
            # Сохраняем детали
            self.redis_client.hset(f"driver:location:{driver_id}", mapping={
                "latitude": str(lat),
                "longitude": str(lon),
                "updated_at": "2024-01-15T12:00:00Z"
            })
            print(f"✅ Driver {driver_id} added to Redis")
        except Exception as e:
            print(f"❌ Redis error (add): {e}")

    def remove_driver_from_redis(self, driver_id: str):
        """Удалить водителя из Redis при is_online = false"""
        try:
            # Удаляем из GEOSET
            self.redis_client.zrem("drivers:online", driver_id)
            
            # Удаляем HASH
            self.redis_client.delete(f"driver:location:{driver_id}")
            print(f"✅ Driver {driver_id} removed from Redis")
        except Exception as e:
            print(f"❌ Redis error (remove): {e}")
