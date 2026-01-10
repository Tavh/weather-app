from unittest.mock import patch
from datetime import datetime, timezone
from app.dtos.weather_dto import WeatherData

def test_refresh_zone_weather(client, auth_header):
    """
    Test refreshing weather for a zone.
    Mocks the internal WeatherService to avoid external API calls during testing.
    """
    # 1. Create Zone
    resp = client.post("/api/v1/zones", headers=auth_header, json={
        "name": "Weather Test",
        "latitude": 50.0,
        "longitude": 10.0
    })
    zone_id = resp.json["id"]
    
    # Verify initial state
    assert resp.json["weather_status"] == "never_fetched"
    
    # 2. Mock WeatherService
    # We patch the class where it is IMPORTED in the service layer, or the class itself
    mock_weather_data = WeatherData(
        temperature_celsius=15.5,
        fetched_at=datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    )
    
    with patch("app.services.weather_service.WeatherService.fetch_current_weather", return_value=mock_weather_data):
        # 3. Refresh Zone
        resp = client.post(f"/api/v1/zones/{zone_id}/refresh", headers=auth_header)
        
        assert resp.status_code == 200
        assert resp.json["weather_status"] == "fresh"
        assert resp.json["temperature"] == 15.5
        assert "2025-01-01" in resp.json["last_fetched_at"]
