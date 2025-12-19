# Fase 2: Ingestión "Pythonic" y Contenerización

## 🎯 Objetivo

Aplicar ingeniería de software pura al flujo de datos. Construir un servicio de ingestión robusto, tipado y contenerizado.

## 📊 Estado: 🟢 Completada (100%)

### Completado
- [x] Modelos Pydantic para respuesta de API OpenWeather
- [x] Cliente HTTP con HTTPX
- [x] Manejo básico de errores
- [x] requirements.txt con dependencias
- [x] Entorno virtual configurado
- [x] Dockerfile para contenerización
- [x] Tests unitarios (14 tests pasando)

## 🛠️ Herramientas Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| **Python 3.11+** | Lenguaje de programación |
| **Pydantic V2** | Validación de datos y contratos |
| **HTTPX** | Cliente HTTP asíncrono |
| **Docker** | Contenerización |
| **pytest** | Testing |

## 📁 Archivos Relevantes

```
weather-dataops-platform/
└── ingestion/
    ├── src/
    │   ├── __init__.py
    │   ├── models.py      # Modelos Pydantic
    │   ├── client.py      # Cliente API
    │   ├── config.py      # Configuración
    │   └── main.py        # Punto de entrada
    ├── tests/
    │   ├── test_models.py
    │   └── test_client.py
    ├── Dockerfile
    └── requirements.txt
```

## 📝 Pasos de Implementación

### Paso 1: Definir Contratos de Datos (Modelos Pydantic)

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

### Paso 2: Construir Cliente API Asíncrono

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

### Paso 3: Gestión de Configuración

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

### Paso 4: Dockerizar

```dockerfile
# ingestion/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "src.main"]
```

### Paso 5: Escribir Tests

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

## 🔐 Gestión de Secretos

**Desarrollo Local**: Usar archivo `.env` (añadir a `.gitignore`)

**GitHub Actions**: Usar secretos del repositorio
```yaml
env:
  OPENWEATHER_API_KEY: ${{ secrets.OPENWEATHER_API_KEY }}
```

**Kubernetes**: Usar K8s Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: weather-secrets
type: Opaque
data:
  openweather-api-key: <clave-codificada-base64>
```

## ✅ Checklist de Completado

- [ ] Modelos Pydantic coinciden con respuesta de API
- [ ] Cliente maneja errores correctamente
- [ ] Lógica de reintentos implementada
- [ ] Logging configurado
- [ ] Imagen Docker se construye correctamente
- [ ] Tests pasan con >80% cobertura
- [ ] Secretos no están hardcodeados

## 🔗 Recursos Relacionados

- [Documentación API OpenWeather](https://openweathermap.org/api)
- [Documentación Pydantic V2](https://docs.pydantic.dev/latest/)
- [Documentación HTTPX](https://www.python-httpx.org/)
- [Tenacity (Librería de Reintentos)](https://tenacity.readthedocs.io/)

## ➡️ Siguiente Fase

Una vez la ingestión funcione, proceder a [Fase 3: Orquestación](./fase-3-orquestacion.md)
