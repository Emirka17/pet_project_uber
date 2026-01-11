from datetime import datetime
import uuid
from models.payment import PaymentRequest, PaymentResponse

class PaymentProcessor:
    @staticmethod
    def process_payment(payment_request: PaymentRequest) -> PaymentResponse:
        try:
            # В тестовом режиме всегда успешная оплата
            # Здесь имитируем успешную обработку
            
            # Можно добавить логику для разных тестовых сценариев
            if payment_request.payment_method_id == "pm_mock_declined":
                status = "failed"
                transaction_id = None
            else:
                status = "succeeded"
                transaction_id = f"txn_mock_{uuid.uuid4().hex[:8]}"
            
            return PaymentResponse(
                payment_id=str(uuid.uuid4()),
                ride_id=payment_request.ride_id,
                status=status,
                amount=payment_request.amount,
                currency=payment_request.currency,
                created_at=datetime.utcnow(),
                transaction_id=transaction_id
            )
            
        except Exception as e:
            # В случае ошибки - возвращаем failed
            return PaymentResponse(
                payment_id=str(uuid.uuid4()),
                ride_id=payment_request.ride_id,
                status="failed",
                amount=payment_request.amount,
                currency=payment_request.currency,
                created_at=datetime.utcnow()
            )
