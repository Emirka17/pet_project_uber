# services/user-service/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.user import User, UserCreate, UserUpdate
from services.user_service import UserService
from config import settings
import psycopg2
from repositories.user_repository import UserRepository

router = APIRouter(prefix="/api/v1/users", tags=["users"])

def get_db_connection():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )

def get_user_service():
    conn = get_db_connection()
    user_repo = UserRepository(conn)
    return UserService(user_repo)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
    users = service.get_users(skip=skip, limit=limit)
    return users

@router.get("/me", response_model=User)
def read_current_user(phone: str, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_phone(phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: str, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, service: UserService = Depends(get_user_service)):
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
