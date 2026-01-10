from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.data.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
