# Phase 2: Pythonic Ingestion & Containerization

## 🎯 Objective

Apply pure software engineering to the data flow. Build a robust, typed, and containerized data ingestion service.

## 📊 Status: 🔴 Not Started (0%)

### Pending
- [ ] Pydantic models for OpenWeather API response
- [ ] Async HTTP client with HTTPX
- [ ] Error handling and retry logic
- [ ] Professional logging setup
- [ ] Dockerfile for the ingestor
- [ ] Unit tests
- [ ] Secrets management for API keys

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Python 3.11+** | Programming language |
| **Pydantic V2** | Data validation and contracts |
| **HTTPX** | Async HTTP client |
| **Docker** | Containerization |
| **pytest** | Testing |

## 📁 Relevant Files

```
weather-dataops-platform/
└── ingestion/
    ├── src/
    │   ├── __init__.py
    │   ├── models.py      # Pydantic models
    │   ├── client.py      # API client
    │   ├── config.py      # Configuration
    │   └── main.py        # Entry point
    ├── tests/
    │   ├── test_models.py
    │   └── test_client.py
    ├── Dockerfile
    └── requirements.txt
```

## 📝 Implementation Steps

### Step 1: Define Data Contracts (Pydantic Models)

```python
# ingestion/src/models.py
from pydantic import BaseModel, Field
from datetime import datetime

class Coordinates(BaseModel):
    lon: float
    lat: float

class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class MainMetrics(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int

class Wind(BaseModel):
    speed: float
    deg: int
    gust: float | None = None

class WeatherResponse(BaseModel):
    coord: Coordinates
    weather: list[Weather]
    main: MainMetrics
    wind: Wind
    dt: int
    name: str
    
    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.dt)
```

### Step 2: Build Async API Client

```python
# ingestion/src/client.py
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .models import WeatherResponse
from .config import settings

class WeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = settings.openweather_api_key
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_current_weather(self, city: str) -> WeatherResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/weather",
                params={
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            return WeatherResponse.model_validate(response.json())
```

### Step 3: Configuration Management

```python
# ingestion/src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openweather_api_key: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "weather"
    postgres_user: str = "weather"
    postgres_password: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Step 4: Dockerize

```dockerfile
# ingestion/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "src.main"]
```

### Step 5: Write Tests

```python
# ingestion/tests/test_models.py
import pytest
from src.models import WeatherResponse

def test_weather_response_validation():
    data = {
        "coord": {"lon": -0.13, "lat": 51.51},
        "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
        "main": {"temp": 15.0, "feels_like": 14.0, "temp_min": 13.0, "temp_max": 17.0, "pressure": 1013, "humidity": 72},
        "wind": {"speed": 3.6, "deg": 180},
        "dt": 1702900000,
        "name": "London"
    }
    response = WeatherResponse.model_validate(data)
    assert response.name == "London"
    assert response.main.temp == 15.0
```

## 🔐 Secrets Management

**Local Development**: Use `.env` file (add to `.gitignore`)

**GitHub Actions**: Use repository secrets
```yaml
env:
  OPENWEATHER_API_KEY: ${{ secrets.OPENWEATHER_API_KEY }}
```

**Kubernetes**: Use K8s Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: weather-secrets
type: Opaque
data:
  openweather-api-key: <base64-encoded-key>
```

## ✅ Completion Checklist

- [ ] Pydantic models match API response
- [ ] Client handles errors gracefully
- [ ] Retry logic implemented
- [ ] Logging configured
- [ ] Docker image builds successfully
- [ ] Tests pass with >80% coverage
- [ ] Secrets not hardcoded

## 🔗 Related Resources

- [OpenWeather API Docs](https://openweathermap.org/api)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [HTTPX Documentation](https://www.python-httpx.org/)
- [Tenacity (Retry Library)](https://tenacity.readthedocs.io/)

## ➡️ Next Phase

Once ingestion is working, proceed to [Phase 3: Orchestration](./phase-3-orchestration.md)
