from enum import Enum as PyEnum

class WeatherStatus(str, PyEnum):
    NEVER_FETCHED = "never_fetched"
    CACHED = "cached"
    FRESH = "fresh"
