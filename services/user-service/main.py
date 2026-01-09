# services/user-service/main.py
from fastapi import FastAPI
from routers import users
from config import settings

app = FastAPI(
    title="User Service",
    description="Микросервис управления пользователями",
    version="1.0.0"
)

app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}

@app.get("/")
async def root():
    return {"message": "User Service - Uber Clone", "version": "1.0.0"}
