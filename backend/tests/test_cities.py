"""City search API tests."""

from unittest.mock import patch, Mock
from tests.constants import DEFAULT_USERNAME, DEFAULT_PASSWORD

def test_search_cities_success(client, auth_header):
    """Test successful city search."""
    # Mock the external geocoding API response
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Paris",
                "country_code": "FR",
                "latitude": 48.8566,
                "longitude": 2.3522
            },
            {
                "name": "Paris",
                "country_code": "US",
                "latitude": 33.6619,
                "longitude": -95.5555
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    
    with patch("app.services.city_search_service.requests.get", return_value=mock_response):
        resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": "Paris"})
        
        assert resp.status_code == 200
        assert "results" in resp.json
        assert len(resp.json["results"]) == 2
        
        # Verify first result
        first = resp.json["results"][0]
        assert first["name"] == "Paris"
        assert first["country_code"] == "FR"
        assert first["latitude"] == 48.8566
        assert first["longitude"] == 2.3522

def test_search_cities_empty_query(client, auth_header):
    """Test city search with empty query parameter."""
    resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": ""})
    
    # Should return 400 or empty results depending on validation
    # OpenAPI validation should catch empty string
    assert resp.status_code in [200, 400]

def test_search_cities_no_results(client, auth_header):
    """Test city search with no matching results."""
    mock_response = Mock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = Mock()
    
    with patch("app.services.city_search_service.requests.get", return_value=mock_response):
        resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": "NonexistentCity12345"})
        
        assert resp.status_code == 200
        assert resp.json["results"] == []

def test_search_cities_requires_authentication(client):
    """Test that city search requires authentication."""
    resp = client.get("/api/v1/cities/search", query_string={"q": "Paris"})
    assert resp.status_code == 401

def test_search_cities_max_results_limit(client, auth_header):
    """Test that city search limits results to 5."""
    # Mock response with more than 5 results
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {"name": f"City{i}", "country_code": "US", "latitude": 40.0 + i, "longitude": -70.0 + i}
            for i in range(10)  # 10 results
        ]
    }
    mock_response.raise_for_status = Mock()
    
    with patch("app.services.city_search_service.requests.get", return_value=mock_response):
        resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": "City"})
        
        assert resp.status_code == 200
        # Should be limited to 5 results
        assert len(resp.json["results"]) == 5

def test_search_cities_api_failure_handling(client, auth_header):
    """Test that API failures return empty list gracefully."""
    import requests
    
    with patch("app.services.city_search_service.requests.get", side_effect=requests.RequestException("API Error")):
        resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": "Paris"})
        
        # Should return 200 with empty results, not raise an error
        assert resp.status_code == 200
        assert resp.json["results"] == []

def test_search_cities_partial_match(client, auth_header):
    """Test city search with partial city name."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Berlin",
                "country_code": "DE",
                "latitude": 52.52,
                "longitude": 13.405
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    
    with patch("app.services.city_search_service.requests.get", return_value=mock_response):
        resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": "Ber"})
        
        assert resp.status_code == 200
        assert len(resp.json["results"]) == 1
        assert resp.json["results"][0]["name"] == "Berlin"

def test_search_cities_missing_country_code(client, auth_header):
    """Test city search when country_code is missing from API response."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Test City",
                "latitude": 50.0,
                "longitude": 10.0
                # country_code missing
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    
    with patch("app.services.city_search_service.requests.get", return_value=mock_response):
        resp = client.get("/api/v1/cities/search", headers=auth_header, query_string={"q": "Test"})
        
        assert resp.status_code == 200
        assert len(resp.json["results"]) == 1
        assert resp.json["results"][0]["country_code"] is None
