# services/ride-service/services/ride_service.py
from typing import List, Optional
from repositories.ride_repository import RideRepository
from models.ride import Ride, RideCreate, RideUpdate

class RideService:
    def __init__(self, ride_repository: RideRepository):
        self.ride_repository = ride_repository
    
    def get_ride(self, ride_id: str) -> Optional[Ride]:
        return self.ride_repository.get_ride(ride_id)
    
    def get_rides(self, skip: int = 0, limit: int = 100) -> List[Ride]:
        return self.ride_repository.get_rides(skip, limit)
    
    def create_ride(self, ride: RideCreate) -> Ride:
        return self.ride_repository.create_ride(ride)
    
    def update_ride(self, ride_id: str, ride: RideUpdate) -> Optional[Ride]:
        return self.ride_repository.update_ride(ride_id, ride)
