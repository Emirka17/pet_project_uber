# services/ride-service/models/ride.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RideBase(BaseModel):
    user_id: str
    driver_id: Optional[str] = None
    vendor_id: int
    pickup_datetime: datetime
    dropoff_datetime: Optional[datetime] = None
    passenger_count: int
    pickup_latitude: float
    pickup_longitude: float
    dropoff_latitude: Optional[float] = None
    dropoff_longitude: Optional[float] = None
    pickup_district: Optional[str] = None
    pickup_neighbourhood: Optional[str] = None
    dropoff_district: Optional[str] = None
    dropoff_neighbourhood: Optional[str] = None
    trip_duration: int
    distance_km: Optional[float] = None
    total_fare: Optional[float] = None
    status: str = "pending"  # pending, assigned, in_progress, completed, cancelled
    pickup_hour: Optional[int] = None
    day_period: Optional[str] = None
    day_name: Optional[str] = None
    weekday_or_weekend: Optional[str] = None
    regular_day_or_holiday: Optional[str] = None
    month: Optional[int] = None
    year: Optional[int] = None
    season: Optional[str] = None

class RideCreate(RideBase):
    pass

class RideUpdate(RideBase):
    pass

class Ride(RideBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
