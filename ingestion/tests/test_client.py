# =============================================================================
# Unit Tests for OpenWeather API Client
# Uses mocking to avoid real API calls during tests
# =============================================================================

import pytest
from unittest.mock import Mock, patch
from src.client import OpenWeatherClient


class TestOpenWeatherClient:
    """Tests for OpenWeatherClient."""

    def test_init_with_api_key(self):
        """Test client initialization with explicit API key."""
        client = OpenWeatherClient(api_key="test_key_123")
        assert client.api_key == "test_key_123"
        client.close()

    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        # Clear any existing env var
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="API key required"):
                OpenWeatherClient()

    def test_init_with_env_var(self):
        """Test client initialization with environment variable."""
        with patch.dict("os.environ", {"OPENWEATHER_API_KEY": "env_key_456"}):
            client = OpenWeatherClient()
            assert client.api_key == "env_key_456"
            client.close()

    def test_context_manager(self):
        """Test that client works as context manager."""
        with OpenWeatherClient(api_key="test_key") as client:
            assert client.api_key == "test_key"
        # Client should be closed after exiting context

    @patch("src.client.httpx.Client")
    def test_get_current_weather_success(self, mock_httpx_client):
        """Test successful weather fetch with mocked response."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "coord": {"lon": -3.70, "lat": 40.42},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
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
            "sys": {"country": "ES", "sunrise": 1702883000, "sunset": 1702917000},
            "name": "Madrid",
            "dt": 1702900000,
            "timezone": 3600
        }
        mock_response.raise_for_status = Mock()
        
        # Configure mock client
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = mock_response
        mock_httpx_client.return_value = mock_client_instance

        # Test
        client = OpenWeatherClient(api_key="test_key")
        weather = client.get_current_weather("Madrid")
        
        assert weather.name == "Madrid"
        assert weather.sys.country == "ES"
        assert weather.temp_celsius == 15.0
        
        client.close()

    def test_base_url_is_correct(self):
        """Test that the base URL is correctly set."""
        assert OpenWeatherClient.BASE_URL == "https://api.openweathermap.org/data/2.5"
