import math
from datetime import datetime
from typing import Tuple

class PricingCalculator:
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance in miles using Haversine formula"""
        R = 3958.8  # Earth radius in miles
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon/2) * math.sin(delta_lon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

    @staticmethod
    def get_surge_multiplier(pickup_datetime: datetime) -> float:
        """Simple surge pricing based on time of day"""
        hour = pickup_datetime.hour
        
        # Peak hours: 7-9 AM, 5-7 PM
        if (7 <= hour <= 9) or (17 <= hour <= 19):
            return 1.5
        # Late night: 10 PM - 6 AM
        elif hour >= 22 or hour <= 6:
            return 1.2
        else:
            return 1.0

    @staticmethod
    def calculate_pricing(
        pickup_lat: float,
        pickup_lon: float,
        dropoff_lat: float,
        dropoff_lon: float,
        pickup_datetime: datetime
    ) -> dict:
        # Calculate distance
        distance = PricingCalculator.calculate_distance(
            pickup_lat, pickup_lon, dropoff_lat, dropoff_lon
        )
        
        # Calculate time (assume average speed 30 mph)
        estimated_time_minutes = (distance / 30) * 60
        
        # Base pricing
        base_fare = 2.50
        distance_rate = 1.75  # per mile
        time_rate = 0.30      # per minute
        
        distance_fare = distance * distance_rate
        time_fare = estimated_time_minutes * time_rate
        
        # Surge pricing
        surge_multiplier = PricingCalculator.get_surge_multiplier(pickup_datetime)
        
        total_amount = (base_fare + distance_fare + time_fare) * surge_multiplier
        
        return {
            "base_fare": round(base_fare, 2),
            "distance_fare": round(distance_fare, 2),
            "time_fare": round(time_fare, 2),
            "surge_multiplier": round(surge_multiplier, 2),
            "total_amount": round(total_amount, 2),
            "currency": "USD"
        }
