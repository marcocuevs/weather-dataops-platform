# Weather DataOps Platform

A learning-focused project to build a complete data platform using modern DevOps, DataOps, and Data Engineering tools.

## 🎯 Project Goal

Build a clonable, automated data platform that:
- Extracts weather data from OpenWeather API
- Processes it with software engineering best practices
- Visualizes insights through dashboards
- All orchestrated under DevOps principles

## 📊 Current Status

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Infrastructure | 🟢 Completed | 100% |
| Phase 2: Ingestion | 🟢 Completed | 100% |
| Phase 3: Orchestration | 🟢 Completed | 100% |
| Phase 4: Transformation | 🔴 Not Started | 0% |
| Phase 5: Visualization | 🔴 Not Started | 0% |

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA FLOW                                 │
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
│                      │ Orchestrator│                             │
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

## 📚 Documentation

- **[Tooling Guide](./tooling-guide.md)** - Complete stack reference
- **[Architecture](./architecture.md)** - Detailed system design
- **[Getting Started](./getting-started.md)** - Quick start guide

### Phase Documentation
- [Phase 1: Infrastructure](./phases/phase-1-infrastructure.md)
- [Phase 2: Ingestion](./phases/phase-2-ingestion.md)
- [Phase 3: Orchestration](./phases/phase-3-orchestration.md)
- [Phase 4: Transformation](./phases/phase-4-transformation.md)
- [Phase 5: Visualization](./phases/phase-5-visualization.md)

## 🛠️ Tech Stack Summary

| Category | Tools |
|----------|-------|
| **IaC** | Terraform |
| **Containers** | Docker, Kind (K8s) |
| **Ingestion** | Python, HTTPX, Pydantic |
| **Orchestration** | Dagster |
| **Transformation** | dbt |
| **Storage** | PostgreSQL, DuckDB |
| **Visualization** | Apache Superset |
| **Data Governance** | DataHub |
| **CI/CD** | GitHub Actions |

## 📁 Project Structure

```
weather-dataops-platform/
├── .github/workflows/    # CI/CD pipelines
├── docs/                 # Documentation (EN/ES)
├── infra/                # Terraform IaC
├── ingestion/            # Python data ingestion
├── orchestration/        # Dagster pipelines
├── transformations/      # dbt models
└── scripts/              # Utility scripts
```

---

📖 [Documentación en Español](../es/README.md)
