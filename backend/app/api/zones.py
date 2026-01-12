import connexion
from typing import List, Dict, Tuple, Any
from app.services.zone_service import ZoneService
from app.dtos.zone_dto import ZoneCreate, ZoneUpdate
from app.core.database import get_session

def _get_user_id() -> int:
def _get_user_id() -> int:
    """Extracts user ID from the validated security context (JWT subject)."""
    token_info = connexion.context.get('token_info')
    return int(token_info['sub'])

def list_zones() -> Tuple[List[Dict[str, Any]], int]:
    """Returns all zones owned by the authenticated user. Implicitly filters by tenant."""
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        zones = service.list_zones()
        return [z.model_dump() for z in zones], 200

def create_zone(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """Provisions a new zone for the user. Initializes associated weather data structures."""
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        dto = ZoneCreate(**body)
        
        created = service.create_zone(dto)
        return created.model_dump(), 201

def get_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    """Retrieves zone details by ID. Enforces strict ownership validation."""
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        zone = service.get_zone(zone_id)
        return zone.model_dump(), 200

def update_zone(zone_id: int, body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """Modifies an existing zone. Validates constraints before applying partial or full updates."""
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        dto = ZoneUpdate(**body)
        
        updated = service.update_zone(zone_id, dto)
        return updated.model_dump(), 200

def delete_zone(zone_id: int) -> Tuple[None, int]:
    """Permanently removes a zone. Fails if the user does not own the resource."""
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        service.delete_zone(zone_id)
        return None, 204

def refresh_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    """Triggers an on-demand weather data refresh from the external provider."""
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        refreshed = service.refresh_zone(zone_id)
        return refreshed.model_dump(), 200
