import logging
from typing import List
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound
from app.repo.zone_repository import ZoneRepository
from app.models.zone import Zone
from app.dtos.zone_dto import ZoneCreate, ZoneUpdate, ZoneResponse
from app.core.enums import WeatherStatus

logger = logging.getLogger(__name__)

class ZoneService:
    def __init__(self, session: Session, user_id: int):
        self.repo = ZoneRepository(session, user_id)
        self.user_id = user_id

    def create_zone(self, dto: ZoneCreate) -> ZoneResponse:
        logger.info(f"Creating zone '{dto.name}' for user {self.user_id}")
        new_zone = Zone(
            name=dto.name,
            latitude=dto.latitude,
            longitude=dto.longitude,
            weather_status=WeatherStatus.NEVER_FETCHED
        )
        created_zone = self.repo.create(new_zone)
        logger.info(f"Zone created successfully (id={created_zone.id})")
        return ZoneResponse.model_validate(created_zone)

    def list_zones(self) -> List[ZoneResponse]:
        zones = self.repo.get_all()
        return [ZoneResponse.model_validate(z) for z in zones]

    def get_zone(self, zone_id: int) -> ZoneResponse:
        zone = self._get_owned_zone_or_404(zone_id)
        return ZoneResponse.model_validate(zone)

    def update_zone(self, zone_id: int, dto: ZoneUpdate) -> ZoneResponse:
        zone = self._get_owned_zone_or_404(zone_id)
        
        logger.info(f"Updating zone {zone_id} for user {self.user_id}")
        zone.name = dto.name
        zone.latitude = dto.latitude
        zone.longitude = dto.longitude
        zone.weather_status = WeatherStatus.NEVER_FETCHED
        zone.temperature = None
        zone.last_fetched_at = None
        
        updated_zone = self.repo.update(zone)
        return ZoneResponse.model_validate(updated_zone)

    def delete_zone(self, zone_id: int) -> None:
        logger.info(f"Deleting zone {zone_id} for user {self.user_id}")
        zone = self._get_owned_zone_or_404(zone_id)
        self.repo.delete(zone)
        logger.info(f"Zone {zone_id} deleted")
            
    def refresh_zone(self, zone_id: int) -> ZoneResponse:
        zone = self._get_owned_zone_or_404(zone_id)
        
        logger.info(f"Refreshing weather for zone {zone_id}")
        # External Service Call
        from app.services.weather_service import WeatherService
        weather_service = WeatherService()
        
        weather_data = weather_service.fetch_current_weather(zone.latitude, zone.longitude)
        
        # Update Zone State
        zone.temperature = weather_data.temperature_celsius
        zone.last_fetched_at = weather_data.fetched_at
        zone.weather_status = WeatherStatus.FRESH
        
        updated_zone = self.repo.update(zone)
        logger.info(f"Weather refreshed for zone {zone_id} (temp={zone.temperature})")
        return ZoneResponse.model_validate(updated_zone)

    def _get_owned_zone_or_404(self, zone_id: int) -> Zone:
        """Helper to retrieve a zone and ensure ownership, or raise 404."""
        zone = self.repo.get_by_id(zone_id)
        if not zone:
            raise NotFound(description=f"Zone {zone_id} not found")
        return zone
