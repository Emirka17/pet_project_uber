# services/user-service/models/user.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    phone: str
    name: Optional[str] = None
    email: Optional[str] = None
    rating: float = 5.00

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: str
    total_rides: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True
