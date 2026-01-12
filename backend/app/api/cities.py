from typing import Dict, Tuple, Any
import logging
from app.services.city_search_service import CitySearchService
from app.dtos.city_dto import CitySearchResponse

logger = logging.getLogger(__name__)

def search_cities(q: str) -> Tuple[Dict[str, Any], int]:
    """Proxies external geocoding provider. Handles upstream timeouts gracefully by returning empty results."""
    logger.info(f"City search requested for query: {q}")
    
    service = CitySearchService()
    results = service.search_cities(q)
    
    response_dto = CitySearchResponse(results=results)
    logger.info(f"Returning {len(results)} city results for query: {q}")
    
    return response_dto.model_dump(), 200
