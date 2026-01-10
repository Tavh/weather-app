from datetime import datetime
from pydantic import BaseModel

class WeatherData(BaseModel):
    temperature_celsius: float
    fetched_at: datetime
