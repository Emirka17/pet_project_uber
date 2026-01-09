# services/driver-service/services/driver_service.py
from typing import List, Optional
from repositories.driver_repository import DriverRepository
from models.driver import Driver, DriverCreate, DriverUpdate

class DriverService:
    def __init__(self, driver_repository: DriverRepository):
        self.driver_repository = driver_repository
    
    def get_driver(self, driver_id: str) -> Optional[Driver]:
        return self.driver_repository.get_driver(driver_id)
    
    def get_driver_by_phone(self, phone: str) -> Optional[Driver]:
        return self.driver_repository.get_driver_by_phone(phone)
    
    def get_drivers(self, skip: int = 0, limit: int = 100) -> List[Driver]:
        return self.driver_repository.get_drivers(skip, limit)
    
    def create_driver(self, driver: DriverCreate) -> Driver:
        existing_driver = self.driver_repository.get_driver_by_phone(driver.phone)
        if existing_driver:
            raise ValueError(f"Driver with phone {driver.phone} already exists")
        
        return self.driver_repository.create_driver(driver)
    
    def update_driver(self, driver_id: str, driver: DriverUpdate) -> Optional[Driver]:
        return self.driver_repository.update_driver(driver_id, driver)
    
    def delete_driver(self, driver_id: str) -> bool:
        return self.driver_repository.delete_driver(driver_id)
