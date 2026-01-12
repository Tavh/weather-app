from sqlalchemy.orm import Session, Query
from typing import Type, TypeVar, Generic

T = TypeVar("T")

class BaseRepository:
    """Encapsulates SQLAlchemy session management. Acts as the transaction boundary adapter."""
    def __init__(self, session: Session):
        self.session = session

class UserScopedRepository(BaseRepository, Generic[T]):
    """Abstract base for tenant-specific data access. Structurally enforces data isolation by creating a mandatory filter predicate."""
    def __init__(self, session: Session, user_id: int):
        super().__init__(session)
        self.user_id = user_id

    def _base_query(self, model_cls: Type[T]) -> Query:
        """Constructs the root query with mandatory user clauses. Prevents accidental cross-tenant data leakage."""
        return self.session.query(model_cls).filter(model_cls.user_id == self.user_id)
