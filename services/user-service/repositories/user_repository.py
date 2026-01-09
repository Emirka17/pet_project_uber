# services/user-service/repositories/user_repository.py
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from models.user import User, UserCreate, UserUpdate

class UserRepository:
    def __init__(self, connection):
        self.conn = connection
    
    def get_user(self, user_id: str) -> Optional[User]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM users WHERE id = %s", 
                (user_id,)
            )
            row = cur.fetchone()
            if row:
                return User(**row)
        return None
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM users WHERE phone = %s", 
                (phone,)
            )
            row = cur.fetchone()
            if row:
                return User(**row)
        return None
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, skip)
            )
            rows = cur.fetchall()
            return [User(**row) for row in rows]
    
    def create_user(self, user: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO users (id, phone, name, email, rating, total_rides, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                RETURNING *
                """,
                (user_id, user.phone, user.name, user.email, user.rating, 0)
            )
            row = cur.fetchone()
            self.conn.commit()
            return User(**row)
    
    def update_user(self, user_id: str, user: UserUpdate) -> Optional[User]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE users 
                SET name = %s, email = %s, rating = %s
                WHERE id = %s
                RETURNING *
                """,
                (user.name, user.email, user.rating, user_id)
            )
            row = cur.fetchone()
            if row:
                self.conn.commit()
                return User(**row)
            return None
    
    def delete_user(self, user_id: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s",
                (user_id,)
            )
            self.conn.commit()
            return cur.rowcount > 0
