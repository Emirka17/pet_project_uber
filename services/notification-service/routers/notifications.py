from fastapi import APIRouter, HTTPException
from models.notification import PushNotification
from services.sender import NotificationSender

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

@router.post("/push")
def send_push(push_notification: PushNotification):
    try:
        result = NotificationSender.send_push_notification(push_notification)
        return {"message": "Notification sent successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")
