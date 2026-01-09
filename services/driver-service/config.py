# services/driver-service/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "uber")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "uber")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "uber_secret_password")
    
    # Сервис
    DRIVER_SERVICE_PORT: int = int(os.getenv("DRIVER_SERVICE_PORT", 8002))
    
    class Config:
        case_sensitive = True

settings = Settings()
