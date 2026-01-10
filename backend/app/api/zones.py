from typing import List, Dict, Tuple, Any, Optional

# Stub controller for Zones

def list_zones() -> Tuple[List[Dict[str, Any]], int]:
    return [], 200

def create_zone(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    # Must match ZoneResponse schema: id, name, latitude, longitude + readonly fields
    result = {
        "id": 1, 
        "name": body.get("name", "Stub Zone"),
        "latitude": body.get("latitude", 0.0),
        "longitude": body.get("longitude", 0.0),
        "temperature": None,
        "last_fetched_at": None,
        "weather_status": "never_fetched"
    }
    return result, 201

def get_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    result = {
        "id": zone_id, 
        "name": "Stub Zone",
        "latitude": 48.85,
        "longitude": 2.35,
        "temperature": 20.0,
        "last_fetched_at": "2023-10-10T10:00:00Z",
        "weather_status": "cached"
    }
    return result, 200

def update_zone(zone_id: int, body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    result = {
        "id": zone_id, 
        "name": body.get("name", "Updated Stub"),
        # Update payload only has name, lat, long
        "latitude": body.get("latitude", 48.85),
        "longitude": body.get("longitude", 2.35),
        "temperature": None,
        "last_fetched_at": None,
        "weather_status": "never_fetched"
    }
    return result, 200

def delete_zone(zone_id: int) -> Tuple[None, int]:
    return None, 204

def refresh_zone(zone_id: int) -> Tuple[Dict[str, Any], int]:
    result = {
        "id": zone_id, 
        "name": "Refreshed Stub",
        "latitude": 48.85,
        "longitude": 2.35,
        "temperature": 15.5,
        "last_fetched_at": "2023-10-27T10:00:00Z",
        "weather_status": "fresh"
    }
    return result, 200
