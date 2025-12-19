# =============================================================================
# Unit Tests for Pydantic Models
# Tests that our data contracts correctly validate API responses
# =============================================================================

import pytest
from src.models import (
    Coordinates,
    WeatherCondition,
    MainMetrics,
    WeatherResponse,
)


class TestCoordinates:
    """Tests for Coordinates model."""

    def test_valid_coordinates(self):
        coords = Coordinates(lon=-3.70, lat=40.42)
        assert coords.lon == -3.70
        assert coords.lat == 40.42

    def test_invalid_coordinates_missing_field(self):
        with pytest.raises(Exception):
            Coordinates.model_validate({"lon": -3.70})  # Missing lat


class TestWeatherCondition:
    """Tests for WeatherCondition model."""

    def test_valid_weather_condition(self):
        condition = WeatherCondition(
            id=800,
            main="Clear",
            description="clear sky",
            icon="01d"
        )
        assert condition.main == "Clear"
        assert condition.description == "clear sky"


class TestMainMetrics:
    """Tests for MainMetrics model."""

    def test_valid_main_metrics(self):
        metrics = MainMetrics(
            temp=288.15,
            feels_like=287.0,
            temp_min=286.0,
            temp_max=290.0,
            pressure=1013,
            humidity=72
        )
        assert metrics.temp == 288.15
        assert metrics.humidity == 72


class TestWeatherResponse:
    """Tests for the complete WeatherResponse model."""

    @pytest.fixture
    def sample_api_response(self):
        """Sample response matching OpenWeather API structure."""
        return {
            "coord": {"lon": -3.70, "lat": 40.42},
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "main": {
                "temp": 288.15,
                "feels_like": 287.0,
                "temp_min": 286.0,
                "temp_max": 290.0,
                "pressure": 1013,
                "humidity": 72
            },
            "wind": {"speed": 3.6, "deg": 180},
            "clouds": {"all": 0},
            "sys": {
                "country": "ES",
                "sunrise": 1702883000,
                "sunset": 1702917000
            },
            "name": "Madrid",
            "dt": 1702900000,
            "timezone": 3600
        }

    def test_valid_weather_response(self, sample_api_response):
        """Test that a valid API response is correctly parsed."""
        response = WeatherResponse.model_validate(sample_api_response)
        
        assert response.name == "Madrid"
        assert response.sys.country == "ES"
        assert response.main.temp == 288.15
        assert response.coord.lat == 40.42
        assert len(response.weather) == 1
        assert response.weather[0].main == "Clear"

    def test_temp_celsius_property(self, sample_api_response):
        """Test the temperature conversion property."""
        response = WeatherResponse.model_validate(sample_api_response)
        
        # 288.15K - 273.15 = 15.0°C
        assert response.temp_celsius == 15.0

    def test_timestamp_property(self, sample_api_response):
        """Test the timestamp conversion property."""
        response = WeatherResponse.model_validate(sample_api_response)
        
        assert response.timestamp is not None
        assert response.timestamp.year == 2023

    def test_invalid_response_missing_required_field(self):
        """Test that missing required fields raise validation error."""
        invalid_data = {
            "coord": {"lon": -3.70, "lat": 40.42},
            # Missing other required fields
        }
        
        with pytest.raises(Exception):
            WeatherResponse.model_validate(invalid_data)
