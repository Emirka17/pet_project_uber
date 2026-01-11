from fastapi import APIRouter, HTTPException
from models.pricing import RideRequest, PricingResponse
from services.calculator import PricingCalculator

router = APIRouter(prefix="/api/v1/pricing", tags=["pricing"])

@router.post("/calculate", response_model=PricingResponse)
def calculate_price(ride_request: RideRequest):
    try:
        pricing_data = PricingCalculator.calculate_pricing(
            ride_request.pickup_latitude,
            ride_request.pickup_longitude,
            ride_request.dropoff_latitude,
            ride_request.dropoff_longitude,
            ride_request.pickup_datetime
        )
        return PricingResponse(**pricing_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pricing calculation error: {str(e)}")
