from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import SessionLocal

class UserRepository:
    def __init__(self):
        self._session = SessionLocal()

    def close(self):
        self._session.close()

    def get_by_username(self, username: str) -> Optional[User]:
        return self._session.query(User).filter(User.username == username).first()

    def create(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user
