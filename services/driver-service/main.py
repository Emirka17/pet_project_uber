# services/driver-service/main.py
from fastapi import FastAPI
from routers import drivers
from config import settings

app = FastAPI(
    title="Driver Service",
    description="Микросервис управления водителями",
    version="1.0.0"
)

app.include_router(drivers.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "driver-service"}

@app.get("/")
async def root():
    return {"message": "Driver Service - Uber Clone", "version": "1.0.0"}
