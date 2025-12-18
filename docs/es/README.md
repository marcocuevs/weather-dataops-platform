# Weather DataOps Platform

Proyecto de aprendizaje para construir una plataforma de datos completa usando herramientas modernas de DevOps, DataOps e Ingeniería de Datos.

## 🎯 Objetivo del Proyecto

Construir una plataforma de datos clonable y automatizada que:
- Extraiga datos meteorológicos de la API de OpenWeather
- Los procese con buenas prácticas de ingeniería de software
- Visualice insights a través de dashboards
- Todo orquestado bajo principios DevOps

## 📊 Estado Actual

| Fase | Estado | Progreso |
|------|--------|----------|
| Fase 1: Infraestructura | 🟡 En Progreso | ~30% |
| Fase 2: Ingestión | 🔴 No Iniciada | 0% |
| Fase 3: Orquestación | 🔴 No Iniciada | 0% |
| Fase 4: Transformación | 🔴 No Iniciada | 0% |
| Fase 5: Visualización | 🔴 No Iniciada | 0% |

## 🏗️ Visión General de la Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLUJO DE DATOS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  OpenWeather API                                                 │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Python    │    │  PostgreSQL │    │     dbt     │          │
│  │  Ingestor   │───▶│   (Bronze)  │───▶│  Transform  │          │
│  │   (HTTPX)   │    │             │    │ Silver/Gold │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│       │                                       │                  │
│       │              ┌─────────────┐          │                  │
│       └─────────────▶│   Dagster   │◀─────────┘                  │
│                      │ Orquestador │                             │
│                      └─────────────┘                             │
│                             │                                    │
│                             ▼                                    │
│                      ┌─────────────┐                             │
│                      │   Apache    │                             │
│                      │   Superset  │                             │
│                      └─────────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📚 Documentación

- **[Guía de Herramientas](./guia-herramientas.md)** - Referencia completa del stack
- **[Arquitectura](./arquitectura.md)** - Diseño detallado del sistema
- **[Primeros Pasos](./primeros-pasos.md)** - Guía de inicio rápido

### Documentación por Fases
- [Fase 1: Infraestructura](./fases/fase-1-infraestructura.md)
- [Fase 2: Ingestión](./fases/fase-2-ingestion.md)
- [Fase 3: Orquestación](./fases/fase-3-orquestacion.md)
- [Fase 4: Transformación](./fases/fase-4-transformacion.md)
- [Fase 5: Visualización](./fases/fase-5-visualizacion.md)

## 🛠️ Resumen del Stack Tecnológico

| Categoría | Herramientas |
|-----------|--------------|
| **IaC** | Terraform |
| **Contenedores** | Docker, Kind (K8s) |
| **Ingestión** | Python, HTTPX, Pydantic |
| **Orquestación** | Dagster |
| **Transformación** | dbt |
| **Almacenamiento** | PostgreSQL, DuckDB |
| **Visualización** | Apache Superset |
| **Data Governance** | DataHub |
| **CI/CD** | GitHub Actions |

## 📁 Estructura del Proyecto

```
weather-dataops-platform/
├── .github/workflows/    # Pipelines CI/CD
├── docs/                 # Documentación (EN/ES)
├── infra/                # Terraform IaC
├── ingestion/            # Ingestión de datos en Python
├── orchestration/        # Pipelines de Dagster
├── transformations/      # Modelos dbt
└── scripts/              # Scripts de utilidad
```

---

📖 [English Documentation](../en/README.md)
