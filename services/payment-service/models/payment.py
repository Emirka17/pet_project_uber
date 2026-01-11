from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class PaymentRequest(BaseModel):
    ride_id: str
    user_id: str
    amount: float
    currency: str = "USD"
    payment_method_id: str  # Stripe payment method

class PaymentResponse(BaseModel):
    payment_id: str
    ride_id: str
    status: str
    amount: float
    currency: str
    created_at: datetime
    transaction_id: Optional[str] = None

class PaymentEvent(BaseModel):
    payment_id: str
    ride_id: str
    user_id: str
    amount: float
    currency: str
    status: str
    timestamp: datetime
