from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationEvent(BaseModel):
    event_type: str
    user_id: str
    message: str
    title: Optional[str] = None
    timestamp: datetime
    metadata: Optional[dict] = None

class PushNotification(BaseModel):
    user_id: str
    title: str
    message: str
    data: Optional[dict] = None
