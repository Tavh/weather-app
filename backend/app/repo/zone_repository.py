from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.repo.base_repository import UserScopedRepository

class ZoneRepository(UserScopedRepository[Zone]):
    # Enforces tenant isolation by implicitly filtering all queries by user_id.
    def __init__(self, session: Session, user_id: int):
        super().__init__(session, user_id)

    def create(self, zone: Zone) -> Zone:
        """Create a new zone."""
        # Ensure the zone is assigned to the current user (double-check)
        zone.user_id = self.user_id
        self.session.add(zone)
        self.session.flush()
        self.session.refresh(zone)
        return zone

    def get_by_id(self, zone_id: int) -> Optional[Zone]:
        """Get a zone by ID, ensuring it belongs to the authenticated user."""
        return self._base_query(Zone).filter(Zone.id == zone_id).first()

    def get_all(self) -> List[Zone]:
        """Get all zones for the authenticated user."""
        return self._base_query(Zone).all()

    def update(self, zone: Zone) -> Zone:
        """Commit changes to an attached zone object."""
        self.session.flush()
        self.session.refresh(zone)
        return zone

    def delete(self, zone: Zone) -> None:
        """Delete a zone."""
        self.session.delete(zone)
        self.session.flush()
