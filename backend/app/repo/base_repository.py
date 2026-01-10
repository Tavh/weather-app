from sqlalchemy.orm import Session, Query
from typing import Type, TypeVar, Generic

T = TypeVar("T")

class BaseRepository:
    """
    Base repository that manages the database session.
    Responsibilities:
    - Hold the session
    - Provide access to session for commit/add
    """
    def __init__(self, session: Session):
        self.session = session

class UserScopedRepository(BaseRepository, Generic[T]):
    """
    Base repository for user-owned data.
    Enforces that all queries are filtered by user_id.
    """
    def __init__(self, session: Session, user_id: int):
        super().__init__(session)
        self.user_id = user_id

    def _base_query(self, model_cls: Type[T]) -> Query:
        """
        Returns a query scoped to the current user.
        """
        return self.session.query(model_cls).filter(model_cls.user_id == self.user_id)
