# services/driver-service/models/driver.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DriverBase(BaseModel):
    phone: str
    name: str
    email: Optional[str] = None
    license_number: str
    car_model: Optional[str] = None
    car_plate: Optional[str] = None
    car_color: Optional[str] = None
    rating: float = 5.00
    total_rides: int = 0
    is_online: bool = False
    is_busy: bool = False
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None

class DriverCreate(DriverBase):
    pass

class DriverUpdate(DriverBase):
    pass

class Driver(DriverBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
