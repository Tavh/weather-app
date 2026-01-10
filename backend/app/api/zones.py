import connexion
from typing import List, Dict, Tuple, Any
from app.services.zone_service import ZoneService
from app.dtos.zone_dto import ZoneCreate, ZoneUpdate
from app.core.database import get_session

def _get_user_id() -> int:
    """Helper to extract user_id from the secure context."""
    token_info = connexion.context.get('token_info')
    return int(token_info['sub'])

def list_zones() -> Tuple[List[Dict[str, Any]], int]:
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        zones = service.list_zones()
        return [z.model_dump() for z in zones], 200

def create_zone(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        # Pydantic validation
        dto = ZoneCreate(**body)
        
        created = service.create_zone(dto)
        return created.model_dump(), 201

def get_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        zone = service.get_zone(zone_id)
        return zone.model_dump(), 200

def update_zone(zone_id: int, body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        # Pydantic validation
        dto = ZoneUpdate(**body)
        
        updated = service.update_zone(zone_id, dto)
        return updated.model_dump(), 200

def delete_zone(zone_id: int) -> Tuple[None, int]:
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        service.delete_zone(zone_id)
        return None, 204

def refresh_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        user_id = _get_user_id()
        service = ZoneService(session, user_id)
        refreshed = service.refresh_zone(zone_id)
        return refreshed.model_dump(), 200
