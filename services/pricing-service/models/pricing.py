from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RideRequest(BaseModel):
    pickup_latitude: float
    pickup_longitude: float
    dropoff_latitude: float
    dropoff_longitude: float
    passenger_count: int
    pickup_datetime: datetime

class PricingResponse(BaseModel):
    base_fare: float
    distance_fare: float
    time_fare: float
    surge_multiplier: float
    total_amount: float
    currency: str = "USD"
