from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ZoneCreate(BaseModel):
    name: str = Field(..., min_length=1, example="Home")
    country_code: Optional[str] = Field(None, max_length=2, example="FR")
    latitude: float = Field(..., ge=-90, le=90, example=48.8566)
    longitude: float = Field(..., ge=-180, le=180, example=2.3522)

class ZoneUpdate(BaseModel):
    name: str = Field(..., min_length=1, example="Home Updated")
    country_code: Optional[str] = Field(None, max_length=2, example="FR")
    latitude: float = Field(..., ge=-90, le=90, example=48.8566)
    longitude: float = Field(..., ge=-180, le=180, example=2.3522)

class ZoneResponse(BaseModel):
    id: int
    name: str
    country_code: Optional[str] = None
    latitude: float
    longitude: float
    temperature: Optional[float] = None
    last_fetched_at: Optional[datetime] = None
    weather_status: str = Field(..., pattern="^(never_fetched|cached|fresh)$")

    class Config:
        from_attributes = True
