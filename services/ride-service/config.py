# services/ride-service/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "uber")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "uber")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "uber_secret_password")
    
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
    
    RIDE_SERVICE_PORT: int = int(os.getenv("RIDE_SERVICE_PORT", 8003))
    
    class Config:
        case_sensitive = True

settings = Settings()
