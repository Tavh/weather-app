from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.enums import WeatherStatus

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    country_code = Column(String(2), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=True)
    last_fetched_at = Column(DateTime, nullable=True)
    weather_status = Column(Enum(WeatherStatus, name="weather_status_enum"), default=WeatherStatus.NEVER_FETCHED, nullable=False)

    user = relationship("User", back_populates="zones")