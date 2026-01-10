from typing import Optional
from pydantic import BaseModel, Field

class CitySearchResult(BaseModel):
    """Single city search result from geocoding API."""
    name: str = Field(..., description="City name", example="Berlin")
    country_code: Optional[str] = Field(None, description="ISO country code", example="DE")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude", example=52.52)
    longitude: float = Field(..., ge=-180, le=180, description="Longitude", example=13.405)

class CitySearchResponse(BaseModel):
    """Response containing list of matching cities."""
    results: list[CitySearchResult] = Field(..., description="List of matching cities")
