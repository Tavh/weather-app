from typing import List
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound
from app.repo.zone_repository import ZoneRepository
from app.models.zone import Zone
from app.dtos.zone_dto import ZoneCreate, ZoneUpdate, ZoneResponse
from app.core.enums import WeatherStatus

class ZoneService:
    def __init__(self, session: Session, user_id: int):
        self.repo = ZoneRepository(session, user_id)
        self.user_id = user_id

    def create_zone(self, dto: ZoneCreate) -> ZoneResponse:
        new_zone = Zone(
            name=dto.name,
            latitude=dto.latitude,
            longitude=dto.longitude,
            weather_status=WeatherStatus.NEVER_FETCHED
        )
        # Repository handles setting user_id
        created_zone = self.repo.create(new_zone)
        return ZoneResponse.model_validate(created_zone)

    def list_zones(self) -> List[ZoneResponse]:
        zones = self.repo.get_all()
        return [ZoneResponse.model_validate(z) for z in zones]

    def get_zone(self, zone_id: int) -> ZoneResponse:
        zone = self._get_owned_zone_or_404(zone_id)
        return ZoneResponse.model_validate(zone)

    def update_zone(self, zone_id: int, dto: ZoneUpdate) -> ZoneResponse:
        zone = self._get_owned_zone_or_404(zone_id)
        
        zone.name = dto.name
        zone.latitude = dto.latitude
        zone.longitude = dto.longitude
        # In a real app, changing location might reset weather data
        zone.weather_status = WeatherStatus.NEVER_FETCHED
        zone.temperature = None
        zone.last_fetched_at = None
        
        updated_zone = self.repo.update(zone)
        return ZoneResponse.model_validate(updated_zone)

    def delete_zone(self, zone_id: int) -> None:
        zone = self._get_owned_zone_or_404(zone_id)
        self.repo.delete(zone)
            
    def refresh_zone(self, zone_id: int) -> ZoneResponse:
        zone = self._get_owned_zone_or_404(zone_id)
        
        # External Service Call
        # Note: In a larger app, we might inject this dependency
        from app.services.weather_service import WeatherService
        weather_service = WeatherService()
        
        weather_data = weather_service.fetch_current_weather(zone.latitude, zone.longitude)
        
        # Update Zone State
        zone.temperature = weather_data.temperature_celsius
        zone.last_fetched_at = weather_data.fetched_at
        zone.weather_status = WeatherStatus.FRESH
        
        updated_zone = self.repo.update(zone)
        return ZoneResponse.model_validate(updated_zone)

    def _get_owned_zone_or_404(self, zone_id: int) -> Zone:
        """Helper to retrieve a zone and ensure ownership, or raise 404."""
        zone = self.repo.get_by_id(zone_id)
        if not zone:
            raise NotFound(description=f"Zone {zone_id} not found")
        return zone
