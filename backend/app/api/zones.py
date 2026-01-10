from typing import List, Dict, Tuple, Any, Optional

# Stub controller for Zones

def list_zones() -> Tuple[List[Dict[str, Any]], int]:
    return [], 200

def create_zone(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    return {"id": 1, "name": body["name"]}, 201

def get_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    return {"id": zone_id, "name": "Stub Zone"}, 200

def update_zone(zone_id: int, body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    return {"id": zone_id, "name": body["name"]}, 200

def delete_zone(zone_id: int) -> Tuple[None, int]:
    return None, 204
