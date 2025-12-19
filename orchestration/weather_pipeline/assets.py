# =============================================================================
# Dagster Assets - Data that our pipeline produces
# An Asset is like a "Dataset" in Azure Data Factory
# =============================================================================

import os
import httpx
from dagster import asset, AssetExecutionContext


@asset
def raw_weather_data(context: AssetExecutionContext) -> dict:
    """
    Fetch current weather data from OpenWeather API.
    
    This is a Dagster Asset - it represents a piece of data that we produce.
    Every time this asset runs, it fetches fresh weather data.
    
    Returns:
        dict: Raw weather data from the API
    """
    # Get API key from environment variable
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")
    
    # City to fetch weather for (could be configurable later)
    city = "Madrid"
    
    # Log what we're doing (appears in Dagster UI)
    context.log.info(f"Fetching weather data for {city}")
    
    # Make API request
    with httpx.Client(timeout=30.0) as client:
        response = client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": api_key,
            },
        )
        response.raise_for_status()
        data = response.json()
    
    # Log success
    context.log.info(f"Successfully fetched weather for {data.get('name')}")
    context.log.info(f"Temperature: {data['main']['temp']}K")
    
    return data
