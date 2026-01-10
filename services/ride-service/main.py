# services/ride-service/main.py
from fastapi import FastAPI
from routers import rides
from config import settings

app = FastAPI(
    title="Ride Service",
    description="Микросервис управления поездками",
    version="1.0.0"
)

app.include_router(rides.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ride-service"}

@app.get("/")
async def root():
    return {"message": "Ride Service - Uber Clone", "version": "1.0.0"}
