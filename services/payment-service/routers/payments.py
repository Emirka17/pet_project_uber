from fastapi import APIRouter, HTTPException
from kafka import KafkaProducer
import json
import os
from datetime import datetime
from models.payment import PaymentRequest, PaymentResponse, PaymentEvent
from services.processor import PaymentProcessor
from config import KAFKA_BOOTSTRAP_SERVERS

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])

# Kafka producer
def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v, default=json_serializer).encode('utf-8')
)

@router.post("/process", response_model=PaymentResponse)
def process_payment(payment_request: PaymentRequest):
    try:
        # Process payment
        payment_result = PaymentProcessor.process_payment(payment_request)
        
        # Send event to Kafka
        payment_event = PaymentEvent(
            payment_id=payment_result.payment_id,
            ride_id=payment_result.ride_id,
            user_id=payment_request.user_id,
            amount=payment_result.amount,
            currency=payment_result.currency,
            status=payment_result.status,
            timestamp=datetime.utcnow()
        )
        
        producer.send('payments.processed', payment_event.dict())
        producer.flush()
        
        return payment_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment processing error: {str(e)}")
