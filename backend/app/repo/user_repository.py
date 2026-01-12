from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repo.base_repository import BaseRepository

class UserRepository(BaseRepository):
    """Manages global user entities (not tenant-scoped). Handles identity persistence."""
    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieves user identity for auth flows. Case-sensitivity depends on DB collation."""
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user: User) -> User:
        """Persists new identity. Relies on database constraints to reject duplicate usernames."""
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user
