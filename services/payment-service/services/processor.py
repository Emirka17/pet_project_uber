import stripe
from config import STRIPE_SECRET_KEY
from models.payment import PaymentRequest, PaymentResponse
from datetime import datetime
import uuid

stripe.api_key = STRIPE_SECRET_KEY

class PaymentProcessor:
    @staticmethod
    def process_payment(payment_request: PaymentRequest) -> PaymentResponse:
        try:
            # Create payment intent with Stripe
            intent = stripe.PaymentIntent.create(
                amount=int(payment_request.amount * 100),  # Convert to cents
                currency=payment_request.currency,
                payment_method=payment_request.payment_method_id,
                confirm=True,
                return_url='https://your-app.com/return'
            )
            
            return PaymentResponse(
                payment_id=str(uuid.uuid4()),
                ride_id=payment_request.ride_id,
                status="succeeded" if intent.status == "succeeded" else "failed",
                amount=payment_request.amount,
                currency=payment_request.currency,
                created_at=datetime.utcnow(),
                transaction_id=intent.id if intent.status == "succeeded" else None
            )
            
        except stripe.error.CardError as e:
            # Card was declined
            return PaymentResponse(
                payment_id=str(uuid.uuid4()),
                ride_id=payment_request.ride_id,
                status="failed",
                amount=payment_request.amount,
                currency=payment_request.currency,
                created_at=datetime.utcnow()
            )
        except Exception as e:
            # Other errors
            return PaymentResponse(
                payment_id=str(uuid.uuid4()),
                ride_id=payment_request.ride_id,
                status="failed",
                amount=payment_request.amount,
                currency=payment_request.currency,
                created_at=datetime.utcnow()
            )
