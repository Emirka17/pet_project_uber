# services/ride-service/routers/rides.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.ride import Ride, RideCreate, RideUpdate
from services.ride_service import RideService
from config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
from repositories.ride_repository import RideRepository

router = APIRouter(prefix="/api/v1/rides", tags=["rides"])

def get_db_connection():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )

def get_ride_service():
    conn = get_db_connection()
    ride_repo = RideRepository(conn)
    return RideService(ride_repo)

@router.get("/", response_model=List[Ride])
def read_rides(skip: int = 0, limit: int = 100, service: RideService = Depends(get_ride_service)):
    rides = service.get_rides(skip=skip, limit=limit)
    return rides

@router.get("/{ride_id}", response_model=Ride)
def read_ride(ride_id: str, service: RideService = Depends(get_ride_service)):
    ride = service.get_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@router.post("/", response_model=Ride, status_code=201)
def create_ride(ride: RideCreate, service: RideService = Depends(get_ride_service)):
    return service.create_ride(ride)

@router.put("/{ride_id}", response_model=Ride)
def update_ride(ride_id: str, ride: RideUpdate, service: RideService = Depends(get_ride_service)):
    updated_ride = service.update_ride(ride_id, ride)
    if not updated_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return updated_ride
