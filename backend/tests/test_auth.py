from tests.constants import DEFAULT_USERNAME, DEFAULT_PASSWORD

def test_register_user(client):
    """Test user registration."""
    resp = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "password": DEFAULT_PASSWORD
    })
    assert resp.status_code == 201
    assert resp.json["message"] == "User created successfully"

def test_login_success(client):
    """Test login with correct credentials."""
    # Register first
    client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "password": DEFAULT_PASSWORD
    })
    
    # Login
    resp = client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": DEFAULT_PASSWORD
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json

def test_login_failure(client):
    """Test login with wrong password."""
    # Register first
    client.post("/api/v1/auth/register", json={
        "username": "wrongpwuser",
        "password": DEFAULT_PASSWORD
    })
    
    # Login wrong
    resp = client.post("/api/v1/auth/login", json={
        "username": "wrongpwuser",
        "password": "WRONGpassword"
    })
    assert resp.status_code == 401
