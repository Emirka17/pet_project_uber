# services/user-service/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Добавь эту строку
from routers import users
from config import settings

app = FastAPI(
    title="User Service",
    description="Микросервис управления пользователями",
    version="1.0.0"
)

# Добавь CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Разрешенные origins
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы
    allow_headers=["*"],  # Разрешенные заголовки
)

app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}

@app.get("/")
async def root():
    return {"message": "User Service - Uber Clone", "version": "1.0.0"}
