# services/driver-service/repositories/driver_repository.py
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from models.driver import Driver, DriverCreate, DriverUpdate

class DriverRepository:
    def __init__(self, connection):
        self.conn = connection
    
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
