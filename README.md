# Weather DataOps Platform

A learning-focused project to build a complete data platform using modern **DevOps**, **DataOps**, and **Data Engineering** tools.

[![CI Quality Check](https://github.com/marcocuevs/weather-dataops-platform/actions/workflows/ci.yaml/badge.svg)](https://github.com/marcocuevs/weather-dataops-platform/actions/workflows/ci.yaml)

## Goal

Build a clonable, automated data platform that extracts weather data from OpenWeather API, processes it with software engineering best practices, and visualizes insights through dashboards.

## Current Status

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Infrastructure | In Progress | ~30% |
| Phase 2: Ingestion | Not Started | 0% |
| Phase 3: Orchestration | Not Started | 0% |
| Phase 4: Transformation | Not Started | 0% |
| Phase 5: Visualization | Not Started | 0% |

## Tech Stack

| Category | Tools |
|----------|-------|
| **IaC** | Terraform, Kind (K8s) |
| **Ingestion** | Python, HTTPX, Pydantic |
| **Orchestration** | Dagster |
| **Transformation** | dbt, DuckDB |
| **Storage** | PostgreSQL |
| **Visualization** | Apache Superset |
| **Data Governance** | DataHub |
| **CI/CD** | GitHub Actions, Ruff |

## Project Structure

```
weather-dataops-platform/
├── .github/workflows/    # CI/CD pipelines
├── docs/                 # Documentation (EN/ES)
│   ├── en/              # English docs
│   ├── es/              # Spanish docs
│   └── adr/             # Architecture Decision Records
├── infra/               # Terraform IaC
├── ingestion/           # Python data ingestion
├── orchestration/       # Dagster pipelines
├── transformations/     # dbt models
└── scripts/             # Utility scripts
```

## Documentation

Full documentation is available in both English and Spanish:

- **[English Documentation](./docs/en/README.md)**
- **[Documentacion en Espanol](./docs/es/README.md)**

### Quick Links

| Topic | English | Spanish |
|-------|---------|---------|
| Project Overview | [README](./docs/en/README.md) | [README](./docs/es/README.md) |
| Tooling Guide | [tooling-guide.md](./docs/en/tooling-guide.md) | [guia-herramientas.md](./docs/es/guia-herramientas.md) |
| Phase 1: Infrastructure | [phase-1](./docs/en/phases/phase-1-infrastructure.md) | [fase-1](./docs/es/fases/fase-1-infraestructura.md) |
| Phase 2: Ingestion | [phase-2](./docs/en/phases/phase-2-ingestion.md) | [fase-2](./docs/es/fases/fase-2-ingestion.md) |
| Phase 3: Orchestration | [phase-3](./docs/en/phases/phase-3-orchestration.md) | [fase-3](./docs/es/fases/fase-3-orquestacion.md) |
| Phase 4: Transformation | [phase-4](./docs/en/phases/phase-4-transformation.md) | [fase-4](./docs/es/fases/fase-4-transformacion.md) |
| Phase 5: Visualization | [phase-5](./docs/en/phases/phase-5-visualization.md) | [fase-5](./docs/es/fases/fase-5-visualizacion.md) |

### Architecture Decision Records (ADRs)

- [ADR-001: Monorepo Structure](./docs/adr/001-monorepo-structure.md)
- [ADR-002: Terraform for IaC](./docs/adr/002-terraform-for-iac.md)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/marcocuevs/weather-dataops-platform.git
cd weather-dataops-platform

# See available commands
make help
```

## Data Flow

```
OpenWeather API --> Python Ingestor --> PostgreSQL (Bronze)
                                              |
                                              v
                                     dbt (Silver/Gold)
                                              |
                                              v
                                      Apache Superset
```

## License

MIT License - see [LICENSE](./LICENSE) for details.
