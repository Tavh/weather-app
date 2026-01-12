from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.repo.base_repository import UserScopedRepository

class ZoneRepository(UserScopedRepository[Zone]):
    """Concrete implementation of user-scoped persistence. Guarantees all Zone interactions are strictly specific to the bound user."""
    def __init__(self, session: Session, user_id: int):
        super().__init__(session, user_id)

    def create(self, zone: Zone) -> Zone:
        """Persists new Zone. Forcibly sets `user_id` to repo scope to enforce ownership."""
        zone.user_id = self.user_id
        self.session.add(zone)
        self.session.flush()
        self.session.refresh(zone)
        return zone

    def get_by_id(self, zone_id: int) -> Optional[Zone]:
        """Resolves Zone entity. Returns `None` if ID doesn't exist OR belongs to another tenant."""
        return self._base_query(Zone).filter(Zone.id == zone_id).first()

    def get_all(self) -> List[Zone]:
        """Fetches entire collection for the tenant. Unpaginated."""
        return self._base_query(Zone).all()

    def update(self, zone: Zone) -> Zone:
        """Updates Zone entity (Full Update, not field-by-field)."""
        self.session.flush()
        self.session.refresh(zone)
        return zone

    def delete(self, zone: Zone) -> None:
        """Deletes Zone entity."""
        self.session.delete(zone)
        self.session.flush()
