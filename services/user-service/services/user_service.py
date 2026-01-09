# services/user-service/services/user_service.py
from typing import List, Optional
from repositories.user_repository import UserRepository
from models.user import User, UserCreate, UserUpdate

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repository.get_user(user_id)
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        return self.user_repository.get_user_by_phone(phone)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repository.get_users(skip, limit)
    
    def create_user(self, user: UserCreate) -> User:
        # Проверяем, существует ли пользователь с таким телефоном
        existing_user = self.user_repository.get_user_by_phone(user.phone)
        if existing_user:
            raise ValueError(f"User with phone {user.phone} already exists")
        
        return self.user_repository.create_user(user)
    
    def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        return self.user_repository.update_user(user_id, user)
    
    def delete_user(self, user_id: str) -> bool:
        return self.user_repository.delete_user(user_id)
