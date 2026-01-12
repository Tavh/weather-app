import logging
import requests
from datetime import datetime, timezone
from app.dtos.weather_dto import WeatherData
from app.core.exceptions import WeatherProviderUnavailable
from app.core.config import Config

logger = logging.getLogger(__name__)

class WeatherService:
    # Uses a single provider implementation. 
    # Can be refactored to support multiple providers if requirements change.
    def fetch_current_weather(self, latitude: float, longitude: float) -> WeatherData:
        """
        Fetches current weather for given coordinates from the configured provider.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"
        }

        try:
            url = Config.WEATHER_PROVIDER_BASE_URL
            logger.debug(f"Fetching weather from {url} with params: {params}")

            response = requests.get(
                url, 
                params=params, 
                timeout=Config.WEATHER_PROVIDER_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info("Weather data fetched successfully from provider")
            
            if "current_weather" not in data:
                raise ValueError("Invalid response format from weather provider")

            current = data["current_weather"]
            
            return WeatherData(
                temperature_celsius=current["temperature"],
                fetched_at=datetime.now(timezone.utc)
            )

        except (requests.RequestException, ValueError) as e:
            logger.warning(f"Weather fetch failed: {str(e)}")
            raise WeatherProviderUnavailable(description="Unable to fetch weather data")
