# Phase 3: Orchestration & Storage

## 🎯 Objective

Unite the pieces and give them a logical order. Deploy services to Kubernetes and orchestrate data pipelines with Dagster.

## 📊 Status: 🔴 Not Started (0%)

### Pending
- [ ] Deploy PostgreSQL to Kind cluster
- [ ] Deploy ingestor as K8s CronJob or Deployment
- [ ] Set up Dagster locally
- [ ] Create Dagster assets for ingestion
- [ ] Configure schedules and sensors
- [ ] Implement basic observability (logs, alerts)

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Kubernetes** | Container orchestration |
| **Dagster** | Data pipeline orchestration |
| **PostgreSQL** | Data storage |
| **Terraform** | Infrastructure deployment |

## 📁 Relevant Files

```
weather-dataops-platform/
├── infra/
│   ├── main.tf
│   ├── postgres.tf        # PostgreSQL K8s resources
│   └── ingestor.tf        # Ingestor deployment
└── orchestration/
    └── dagster/
        ├── __init__.py
        ├── assets/
        │   ├── __init__.py
        │   └── weather.py  # Weather data assets
        ├── jobs.py
        ├── schedules.py
        └── repository.py
```

## 📝 Implementation Steps

### Step 1: Deploy PostgreSQL to Kubernetes

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

### Step 2: Set Up Dagster Project

```bash
pip install dagster dagster-webserver dagster-postgres
dagster project scaffold --name weather_orchestration
```

### Step 3: Define Dagster Assets

```python
# orchestration/dagster/assets/weather.py
from dagster import asset, AssetExecutionContext
import asyncio
from ingestion.src.client import WeatherClient
from ingestion.src.models import WeatherResponse

@asset(
    description="Raw weather data from OpenWeather API",
    group_name="bronze"
)
def raw_weather_data(context: AssetExecutionContext) -> dict:
    """Fetch current weather data for configured cities."""
    client = WeatherClient()
    cities = ["Madrid", "Barcelona", "London", "Paris", "Berlin"]
    
    async def fetch_all():
        results = []
        for city in cities:
            try:
                data = await client.get_current_weather(city)
                results.append(data.model_dump())
                context.log.info(f"Fetched weather for {city}")
            except Exception as e:
                context.log.error(f"Failed to fetch {city}: {e}")
        return results
    
    return {"records": asyncio.run(fetch_all())}

@asset(
    deps=[raw_weather_data],
    description="Weather data persisted to PostgreSQL Bronze layer",
    group_name="bronze"
)
def bronze_weather_table(context: AssetExecutionContext, raw_weather_data: dict):
    """Insert raw weather data into PostgreSQL."""
    # Implementation: Insert into bronze.weather_raw table
    context.log.info(f"Inserting {len(raw_weather_data['records'])} records to bronze layer")
    # ... database insertion logic
    return {"rows_inserted": len(raw_weather_data["records"])}
```

### Step 4: Configure Schedules

```python
# orchestration/dagster/schedules.py
from dagster import ScheduleDefinition, define_asset_job

weather_ingestion_job = define_asset_job(
    name="weather_ingestion_job",
    selection=["raw_weather_data", "bronze_weather_table"]
)

hourly_weather_schedule = ScheduleDefinition(
    job=weather_ingestion_job,
    cron_schedule="0 * * * *",  # Every hour
    description="Fetch weather data every hour"
)
```

### Step 5: Create Repository

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

### Step 6: Run Dagster Locally

```bash
cd orchestration/dagster
dagster dev
# Access UI at http://localhost:3000
```

## 🔍 Observability

### Logging Strategy
- **Structured logging**: Use JSON format for easy parsing
- **Log levels**: DEBUG for dev, INFO for prod
- **Context**: Include asset name, run ID, timestamps

### Basic Alerting
```python
from dagster import failure_hook, HookContext

@failure_hook
def notify_on_failure(context: HookContext):
    # Send notification (Slack, email, etc.)
    context.log.error(f"Asset {context.op.name} failed!")
```

## ✅ Completion Checklist

- [ ] PostgreSQL running in Kind cluster
- [ ] Ingestor can connect to PostgreSQL
- [ ] Dagster UI accessible locally
- [ ] Assets execute successfully
- [ ] Schedule triggers on time
- [ ] Logs are structured and useful
- [ ] Basic failure alerts configured

## 🔗 Related Resources

- [Dagster Documentation](https://docs.dagster.io/)
- [Dagster Assets Tutorial](https://docs.dagster.io/concepts/assets/software-defined-assets)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## ➡️ Next Phase

Once orchestration is working, proceed to [Phase 4: Transformation](./phase-4-transformation.md)
