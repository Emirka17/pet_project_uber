# services/ride-service/repositories/ride_repository.py
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from models.ride import Ride, RideCreate, RideUpdate

class RideRepository:
    def __init__(self, connection):
        self.conn = connection
    
    def get_ride(self, ride_id: str) -> Optional[Ride]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM rides WHERE id = %s", (ride_id,))
            row = cur.fetchone()
            return Ride(**row) if row else None
    
    def get_rides(self, skip: int = 0, limit: int = 100) -> List[Ride]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM rides ORDER BY pickup_datetime DESC LIMIT %s OFFSET %s", (limit, skip))
            rows = cur.fetchall()
            return [Ride(**row) for row in rows]
    
    def create_ride(self, ride: RideCreate) -> Ride:
        ride_id = str(uuid.uuid4())
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING *
            """, (
                ride_id, ride.user_id, ride.driver_id, ride.vendor_id,
                ride.pickup_datetime, ride.dropoff_datetime, ride.passenger_count,
                ride.pickup_latitude, ride.pickup_longitude,
                ride.dropoff_latitude, ride.dropoff_longitude,
                ride.pickup_district, ride.pickup_neighbourhood,
                ride.dropoff_district, ride.dropoff_neighbourhood,
                ride.trip_duration, ride.distance_km, ride.total_fare, ride.status,
                ride.pickup_hour, ride.day_period, ride.day_name,
                ride.weekday_or_weekend, ride.regular_day_or_holiday,
                ride.month, ride.year, ride.season
            ))
            row = cur.fetchone()
            self.conn.commit()
            return Ride(**row)
    
    def update_ride(self, ride_id: str, ride: RideUpdate) -> Optional[Ride]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                UPDATE rides SET
                    driver_id = %s, status = %s, dropoff_datetime = %s,
                    dropoff_latitude = %s, dropoff_longitude = %s,
                    distance_km = %s, total_fare = %s
                WHERE id = %s
                RETURNING *
            """, (
                ride.driver_id, ride.status, ride.dropoff_datetime,
                ride.dropoff_latitude, ride.dropoff_longitude,
                ride.distance_km, ride.total_fare, ride_id
            ))
            row = cur.fetchone()
            if row:
                self.conn.commit()
                return Ride(**row)
            return None
