# =============================================================================
# OpenWeather API Client - HTTP client using HTTPX
# HTTPX is like 'requests' but with async support and better typing
# =============================================================================

import os
import httpx
from models import WeatherResponse


class OpenWeatherClient:
    """
    Client to interact with OpenWeather API.
    
    Usage:
        client = OpenWeatherClient(api_key="your_key")
        weather = client.get_current_weather("Madrid")
        print(weather.temp_celsius)
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str | None = None):
        """
        Initialize the client.
        
        Args:
            api_key: OpenWeather API key. If not provided, reads from 
                     OPENWEATHER_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Pass it as argument or set OPENWEATHER_API_KEY env var."
            )
        # Create HTTP client with timeout (good practice)
        self._client = httpx.Client(timeout=30.0)

    def get_current_weather(self, city: str) -> WeatherResponse:
        """
        Get current weather for a city.
        
        Args:
            city: City name (e.g., "Madrid", "London", "New York")
            
        Returns:
            WeatherResponse: Validated weather data
            
        Raises:
            httpx.HTTPStatusError: If API returns an error
        """
        response = self._client.get(
            f"{self.BASE_URL}/weather",
            params={
                "q": city,
                "appid": self.api_key,
            },
        )
        # Raise exception if status code is 4xx or 5xx
        response.raise_for_status()

        # Parse JSON and validate with Pydantic
        # If the data doesn't match the schema, Pydantic raises an error
        return WeatherResponse.model_validate(response.json())

    def get_weather_by_coords(self, lat: float, lon: float) -> WeatherResponse:
        """
        Get current weather by geographic coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            WeatherResponse: Validated weather data
        """
        response = self._client.get(
            f"{self.BASE_URL}/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
            },
        )
        response.raise_for_status()
        return WeatherResponse.model_validate(response.json())

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        """Context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close client when exiting context."""
        self.close()
