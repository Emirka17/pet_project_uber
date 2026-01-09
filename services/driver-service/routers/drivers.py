# services/driver-service/routers/drivers.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.driver import Driver, DriverCreate, DriverUpdate
from services.driver_service import DriverService
from config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
from repositories.driver_repository import DriverRepository

router = APIRouter(prefix="/api/v1/drivers", tags=["drivers"])

def get_db_connection():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )

def get_driver_service():
    conn = get_db_connection()
    driver_repo = DriverRepository(conn)
    return DriverService(driver_repo)

@router.get("/", response_model=List[Driver])
def read_drivers(skip: int = 0, limit: int = 100, service: DriverService = Depends(get_driver_service)):
    drivers = service.get_drivers(skip=skip, limit=limit)
    return drivers

@router.get("/me", response_model=Driver)
def read_current_driver(phone: str, service: DriverService = Depends(get_driver_service)):
    driver = service.get_driver_by_phone(phone)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.get("/{driver_id}", response_model=Driver)
def read_driver(driver_id: str, service: DriverService = Depends(get_driver_service)):
    driver = service.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.post("/", response_model=Driver, status_code=201)
def create_driver(driver: DriverCreate, service: DriverService = Depends(get_driver_service)):
    try:
        return service.create_driver(driver)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{driver_id}", response_model=Driver)
def update_driver(driver_id: str, driver: DriverUpdate, service: DriverService = Depends(get_driver_service)):
    updated_driver = service.update_driver(driver_id, driver)
    if not updated_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return updated_driver

@router.delete("/{driver_id}")
def delete_driver(driver_id: str, service: DriverService = Depends(get_driver_service)):
    success = service.delete_driver(driver_id)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver deleted successfully"}
