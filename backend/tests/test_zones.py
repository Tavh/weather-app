"""Create and list zone tests."""

from tests.constants import (
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    ZONE_A_NAME,
    ZONE_A_LAT,
    ZONE_A_LON,
)

def test_create_and_list_zone(client, auth_header):
    """Test creating a zone and listing it."""
    # 1. Create Zone
    resp = client.post("/api/v1/zones", headers=auth_header, json={
        "name": ZONE_A_NAME,
        "latitude": ZONE_A_LAT,
        "longitude": ZONE_A_LON
    })
    assert resp.status_code == 201, f"Failed to create zone: {resp.data}"
    zone_id = resp.json["id"]
    
    # 2. List Zones
    resp = client.get("/api/v1/zones", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]["id"] == zone_id
    assert resp.json[0]["name"] == ZONE_A_NAME

def test_zone_isolation(client, auth_header):
    """Ensure User A cannot see User B's zones."""
    # User A creates a zone
    client.post("/api/v1/zones", headers=auth_header, json={
        "name": ZONE_A_NAME,
        "latitude": ZONE_A_LAT,
        "longitude": ZONE_A_LON
    })
    
    # User B Registers & Logs in
    import uuid
    user_b_name = f"userb_{uuid.uuid4().hex[:8]}"
    
    # Register B
    resp_reg = client.post("/api/v1/auth/register", json={
        "username": user_b_name, 
        "password": DEFAULT_PASSWORD
    })
    assert resp_reg.status_code == 201, f"User B registration failed: {resp_reg.data}"
    
    # Login B
    resp_login = client.post("/api/v1/auth/login", json={
        "username": user_b_name, 
        "password": DEFAULT_PASSWORD
    })
    assert resp_login.status_code == 200, f"User B login failed: {resp_login.data}"
    
    token_b = resp_login.json["access_token"]
    header_b = {"Authorization": f"Bearer {token_b}"}
    
    # User B Lists Zones -> Should be empty (cannot see A's zone)
    resp = client.get("/api/v1/zones", headers=header_b)
    assert resp.status_code == 200
    assert len(resp.json) == 0

def test_delete_zone(client, auth_header):
    """Test deleting a zone."""
    # Create
    resp = client.post("/api/v1/zones", headers=auth_header, json={
        "name": "Delete Me", 
        "latitude": 0.0, 
        "longitude": 0.0
    })
    zone_id = resp.json["id"]
    
    # Delete
    resp = client.delete(f"/api/v1/zones/{zone_id}", headers=auth_header)
    assert resp.status_code == 204
    
    # Verify Gone
    resp = client.get(f"/api/v1/zones/{zone_id}", headers=auth_header)
    assert resp.status_code == 404

def test_modify_others_zone_fails(client, auth_header):
    """Ensure User A cannot update or delete User B's zone."""
    # 1. User A creates a zone
    resp = client.post("/api/v1/zones", headers=auth_header, json={
        "name": ZONE_A_NAME,
        "latitude": ZONE_A_LAT,
        "longitude": ZONE_A_LON
    })
    assert resp.status_code == 201
    zone_a_id = resp.json["id"]

    # 2. Register & Login User B
    import uuid
    user_b_name = f"userb_{uuid.uuid4().hex[:8]}"
    
    client.post("/api/v1/auth/register", json={
        "username": user_b_name, 
        "password": DEFAULT_PASSWORD
    })
    resp_login = client.post("/api/v1/auth/login", json={
        "username": user_b_name, 
        "password": DEFAULT_PASSWORD
    })
    token_b = resp_login.json["access_token"]
    header_b = {"Authorization": f"Bearer {token_b}"}

    # 3. User B tries to update User A's zone -> Expect 404
    resp = client.put(f"/api/v1/zones/{zone_a_id}", headers=header_b, json={
        "name": "Hacked Zone",
        "latitude": 0.0,
        "longitude": 0.0
    })
    assert resp.status_code == 404

    # 4. User B tries to delete User A's zone -> Expect 404
    resp = client.delete(f"/api/v1/zones/{zone_a_id}", headers=header_b)
    assert resp.status_code == 404

def test_create_zone_invalid_coordinates(client, auth_header):
    """Test validation failure for invalid latitude/longitude."""
    resp = client.post("/api/v1/zones", headers=auth_header, json={
        "name": "Impossible Zone",
        "latitude": 999.0, # Invalid > 90
        "longitude": 0.0
    })
    # Validation error handled by Connexion/Pydantic
    assert resp.status_code == 400

def test_update_zone_lifecycle(client, auth_header):
    """Test full update lifecycle including weather status reset."""
    # 1. Create
    resp = client.post("/api/v1/zones", headers=auth_header, json={
        "name": "Original",
        "latitude": 10.0,
        "longitude": 10.0
    })
    zone_id = resp.json["id"]

    # 2. Update Zone (Move location)
    resp = client.put(f"/api/v1/zones/{zone_id}", headers=auth_header, json={
        "name": "Moved",
        "latitude": 20.0, # Changed
        "longitude": 20.0
    })
    assert resp.status_code == 200
    assert resp.json["name"] == "Moved"
    assert resp.json["weather_status"] == "never_fetched" # Should be reset
