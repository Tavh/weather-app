import logging
import requests
from typing import List
from app.dtos.city_dto import CitySearchResult
from app.core.config import Config

logger = logging.getLogger(__name__)

class CitySearchService:
    """
    Service for searching cities using Open-Meteo Geocoding API.
    This is a non-persistent adapter - no caching or database storage.
    """
    
    MAX_RESULTS = 5
    TIMEOUT_SECONDS = 5
    
    def search_cities(self, query: str) -> List[CitySearchResult]:
        """
        Search for cities by name using Open-Meteo Geocoding API.
        
        Args:
            query: City name to search for
            
        Returns:
            List of CitySearchResult objects (max 5 results)
        """
        if not query or not query.strip():
            logger.warning("Empty search query provided")
            return []
        
        params = {
            "name": query.strip(),
            "count": self.MAX_RESULTS,
            "language": "en",
            "format": "json"
        }
        
        try:
            logger.debug(f"Searching cities with query: {query}")
            response = requests.get(
                Config.CITY_GEOCODING_BASE_URL,
                params=params,
                timeout=self.TIMEOUT_SECONDS
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"City search successful for query: {query}")
            
            # Open-Meteo returns results in 'results' array
            if "results" not in data or not data["results"]:
                logger.debug(f"No results found for query: {query}")
                return []
            
            # Map API response to our DTOs
            cities = []
            for result in data["results"][:self.MAX_RESULTS]:
                cities.append(CitySearchResult(
                    name=result.get("name", ""),
                    country_code=result.get("country_code", None),
                    latitude=float(result.get("latitude", 0)),
                    longitude=float(result.get("longitude", 0))
                ))
            
            logger.debug(f"Returning {len(cities)} city results")
            return cities
            
        except requests.RequestException as e:
            logger.error(f"City search API request failed: {str(e)}")
            # Return empty list on API failure (non-critical feature)
            return []
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Invalid response format from geocoding API: {str(e)}")
            return []
