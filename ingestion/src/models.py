# =============================================================================
# Pydantic Models - Data validation for OpenWeather API responses
# Similar to defining a DataFrame schema, but with automatic validation
# =============================================================================

from datetime import datetime
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Geographic coordinates of the location."""
    lon: float = Field(..., description="Longitude")
    lat: float = Field(..., description="Latitude")


class WeatherCondition(BaseModel):
    """Weather condition details (rain, clouds, etc.)."""
    id: int = Field(..., description="Weather condition ID")
    main: str = Field(..., description="Group of weather parameters (Rain, Snow, etc.)")
    description: str = Field(..., description="Weather condition description")
    icon: str = Field(..., description="Weather icon ID")


class MainMetrics(BaseModel):
    """Main weather metrics (temperature, humidity, pressure)."""
    temp: float = Field(..., description="Temperature in Kelvin")
    feels_like: float = Field(..., description="Human perception of temperature")
    temp_min: float = Field(..., description="Minimum temperature")
    temp_max: float = Field(..., description="Maximum temperature")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    humidity: int = Field(..., description="Humidity percentage")


class Wind(BaseModel):
    """Wind information."""
    speed: float = Field(..., description="Wind speed in m/s")
    deg: int = Field(..., description="Wind direction in degrees")


class Clouds(BaseModel):
    """Cloud coverage."""
    all: int = Field(..., description="Cloudiness percentage")


class SystemInfo(BaseModel):
    """System information from the API."""
    country: str = Field(..., description="Country code (e.g., ES, US)")
    sunrise: int = Field(..., description="Sunrise time (Unix timestamp)")
    sunset: int = Field(..., description="Sunset time (Unix timestamp)")


class WeatherResponse(BaseModel):
    """
    Complete response from OpenWeather Current Weather API.
    Docs: https://openweathermap.org/current
    """
    coord: Coordinates
    weather: list[WeatherCondition]
    main: MainMetrics
    wind: Wind
    clouds: Clouds
    sys: SystemInfo
    name: str = Field(..., description="City name")
    dt: int = Field(..., description="Time of data calculation (Unix timestamp)")
    timezone: int = Field(..., description="Shift in seconds from UTC")

    @property
    def timestamp(self) -> datetime:
        """Convert Unix timestamp to datetime."""
        return datetime.fromtimestamp(self.dt)

    @property
    def temp_celsius(self) -> float:
        """Convert temperature from Kelvin to Celsius."""
        return round(self.main.temp - 273.15, 2)
