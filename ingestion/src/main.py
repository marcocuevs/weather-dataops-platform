# =============================================================================
# Main script - Example of how to use the weather client
# Run this to test the ingestion pipeline
# =============================================================================

from client import OpenWeatherClient


def main():
    """
    Example usage of the OpenWeather client.
    
    Before running, set your API key:
        export OPENWEATHER_API_KEY=your_key_here  (Linux/Mac)
        $env:OPENWEATHER_API_KEY="your_key_here"  (PowerShell)
    """
    # List of cities to fetch weather for
    cities = ["Madrid", "London", "New York", "Tokyo"]

    # Using context manager ensures the client is properly closed
    with OpenWeatherClient() as client:
        for city in cities:
            try:
                weather = client.get_current_weather(city)

                print(f"\n{'='*50}")
                print(f"City: {weather.name} ({weather.sys.country})")
                print(f"{'='*50}")
                print(f"Temperature: {weather.temp_celsius}°C")
                print(f"Feels like: {round(weather.main.feels_like - 273.15, 2)}°C")
                print(f"Humidity: {weather.main.humidity}%")
                print(f"Conditions: {weather.weather[0].description}")
                print(f"Wind: {weather.wind.speed} m/s")
                print(f"Timestamp: {weather.timestamp}")

            except Exception as e:
                print(f"Error fetching weather for {city}: {e}")


if __name__ == "__main__":
    main()
