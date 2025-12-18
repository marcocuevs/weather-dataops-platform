# Fase 3: Orquestación y Almacenamiento

## 🎯 Objetivo

Unir las piezas y darles un orden lógico. Desplegar servicios en Kubernetes y orquestar pipelines de datos con Dagster.

## 📊 Estado: 🔴 No Iniciada (0%)

### Pendiente
- [ ] Desplegar PostgreSQL en clúster Kind
- [ ] Desplegar ingestor como CronJob o Deployment en K8s
- [ ] Configurar Dagster localmente
- [ ] Crear assets de Dagster para ingestión
- [ ] Configurar schedules y sensors
- [ ] Implementar observabilidad básica (logs, alertas)

## 🛠️ Herramientas Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| **Kubernetes** | Orquestación de contenedores |
| **Dagster** | Orquestación de pipelines de datos |
| **PostgreSQL** | Almacenamiento de datos |
| **Terraform** | Despliegue de infraestructura |

## 📁 Archivos Relevantes

```
weather-dataops-platform/
├── infra/
│   ├── main.tf
│   ├── postgres.tf        # Recursos K8s de PostgreSQL
│   └── ingestor.tf        # Deployment del ingestor
└── orchestration/
    └── dagster/
        ├── __init__.py
        ├── assets/
        │   ├── __init__.py
        │   └── weather.py  # Assets de datos meteorológicos
        ├── jobs.py
        ├── schedules.py
        └── repository.py
```

## 📝 Pasos de Implementación

### Paso 1: Desplegar PostgreSQL en Kubernetes

```hcl
# infra/postgres.tf
resource "kubernetes_namespace" "database" {
  metadata {
    name = "database"
  }
}

resource "kubernetes_persistent_volume_claim" "postgres" {
  metadata {
    name      = "postgres-pvc"
    namespace = kubernetes_namespace.database.metadata[0].name
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
  }
}

resource "kubernetes_deployment" "postgres" {
  metadata {
    name      = "postgres"
    namespace = kubernetes_namespace.database.metadata[0].name
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgres"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgres"
        }
      }
      spec {
        container {
          name  = "postgres"
          image = "postgres:15-alpine"
          port {
            container_port = 5432
          }
          env {
            name  = "POSTGRES_DB"
            value = "weather"
          }
          env {
            name = "POSTGRES_PASSWORD"
            value_from {
              secret_key_ref {
                name = "postgres-secret"
                key  = "password"
              }
            }
          }
          volume_mount {
            name       = "postgres-storage"
            mount_path = "/var/lib/postgresql/data"
          }
        }
        volume {
          name = "postgres-storage"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.postgres.metadata[0].name
          }
        }
      }
    }
  }
}
```

### Paso 2: Configurar Proyecto Dagster

```bash
pip install dagster dagster-webserver dagster-postgres
dagster project scaffold --name weather_orchestration
```

### Paso 3: Definir Assets de Dagster

```python
# orchestration/dagster/assets/weather.py
from dagster import asset, AssetExecutionContext
import asyncio
from ingestion.src.client import WeatherClient
from ingestion.src.models import WeatherResponse

@asset(
    description="Datos meteorológicos crudos de la API OpenWeather",
    group_name="bronze"
)
def raw_weather_data(context: AssetExecutionContext) -> dict:
    """Obtener datos meteorológicos actuales para ciudades configuradas."""
    client = WeatherClient()
    cities = ["Madrid", "Barcelona", "London", "Paris", "Berlin"]
    
    async def fetch_all():
        results = []
        for city in cities:
            try:
                data = await client.get_current_weather(city)
                results.append(data.model_dump())
                context.log.info(f"Obtenidos datos de {city}")
            except Exception as e:
                context.log.error(f"Error al obtener {city}: {e}")
        return results
    
    return {"records": asyncio.run(fetch_all())}

@asset(
    deps=[raw_weather_data],
    description="Datos meteorológicos persistidos en capa Bronze de PostgreSQL",
    group_name="bronze"
)
def bronze_weather_table(context: AssetExecutionContext, raw_weather_data: dict):
    """Insertar datos crudos en PostgreSQL."""
    # Implementación: Insertar en tabla bronze.weather_raw
    context.log.info(f"Insertando {len(raw_weather_data['records'])} registros en capa bronze")
    # ... lógica de inserción en base de datos
    return {"rows_inserted": len(raw_weather_data["records"])}
```

### Paso 4: Configurar Schedules

```python
# orchestration/dagster/schedules.py
from dagster import ScheduleDefinition, define_asset_job

weather_ingestion_job = define_asset_job(
    name="weather_ingestion_job",
    selection=["raw_weather_data", "bronze_weather_table"]
)

hourly_weather_schedule = ScheduleDefinition(
    job=weather_ingestion_job,
    cron_schedule="0 * * * *",  # Cada hora
    description="Obtener datos meteorológicos cada hora"
)
```

### Paso 5: Crear Repository

```python
# orchestration/dagster/repository.py
from dagster import Definitions, load_assets_from_modules
from . import assets
from .schedules import hourly_weather_schedule, weather_ingestion_job

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[weather_ingestion_job],
    schedules=[hourly_weather_schedule]
)
```

### Paso 6: Ejecutar Dagster Localmente

```bash
cd orchestration/dagster
dagster dev
# Acceder a UI en http://localhost:3000
```

## 🔍 Observabilidad

### Estrategia de Logging
- **Logging estructurado**: Usar formato JSON para fácil parsing
- **Niveles de log**: DEBUG para dev, INFO para prod
- **Contexto**: Incluir nombre del asset, run ID, timestamps

### Alertas Básicas
```python
from dagster import failure_hook, HookContext

@failure_hook
def notify_on_failure(context: HookContext):
    # Enviar notificación (Slack, email, etc.)
    context.log.error(f"Asset {context.op.name} falló!")
```

## ✅ Checklist de Completado

- [ ] PostgreSQL ejecutándose en clúster Kind
- [ ] Ingestor puede conectar a PostgreSQL
- [ ] UI de Dagster accesible localmente
- [ ] Assets se ejecutan correctamente
- [ ] Schedule se dispara a tiempo
- [ ] Logs son estructurados y útiles
- [ ] Alertas básicas de fallo configuradas

## 🔗 Recursos Relacionados

- [Documentación de Dagster](https://docs.dagster.io/)
- [Tutorial de Assets de Dagster](https://docs.dagster.io/concepts/assets/software-defined-assets)
- [Deployments de Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## ➡️ Siguiente Fase

Una vez la orquestación funcione, proceder a [Fase 4: Transformación](./fase-4-transformacion.md)
