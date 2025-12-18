# Tooling Guide

Complete reference of all tools used in this project, why they were chosen, and learning resources.

## 🏗️ Infrastructure as Code (IaC)

### Terraform
**Purpose**: Provision and manage infrastructure declaratively.

| Aspect | Details |
|--------|---------|
| **Why** | Industry standard, cloud-agnostic, excellent state management |
| **Use Case** | Define Kind cluster, PostgreSQL, and all K8s resources |
| **Alternatives** | Pulumi, CloudFormation, Ansible |

**Learning Resources**:
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

## 🐳 Containerization & Orchestration

### Docker
**Purpose**: Package applications into portable containers.

| Aspect | Details |
|--------|---------|
| **Why** | Standard containerization, reproducible environments |
| **Use Case** | Containerize Python ingestor, dbt, and all services |
| **Alternatives** | Podman, containerd |

### Kind (Kubernetes in Docker)
**Purpose**: Run local Kubernetes clusters for development.

| Aspect | Details |
|--------|---------|
| **Why** | Lightweight, perfect for local dev, mirrors production K8s |
| **Use Case** | Local K8s cluster to deploy all services |
| **Alternatives** | Minikube, k3s, Docker Desktop K8s |

**Learning Resources**:
- [Docker Documentation](https://docs.docker.com/)
- [Kind Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

---

## 🐍 Data Ingestion

### Python 3.11+
**Purpose**: Primary programming language for data pipelines.

### HTTPX
**Purpose**: Modern async HTTP client for API calls.

| Aspect | Details |
|--------|---------|
| **Why** | Async support, HTTP/2, better than requests for modern apps |
| **Use Case** | Call OpenWeather API with retries and error handling |
| **Alternatives** | aiohttp, requests |

### Pydantic V2
**Purpose**: Data validation and settings management using Python type hints.

| Aspect | Details |
|--------|---------|
| **Why** | Type safety, automatic validation, excellent for data contracts |
| **Use Case** | Define and validate API response schemas |
| **Alternatives** | dataclasses, attrs, marshmallow |

**Learning Resources**:
- [HTTPX Documentation](https://www.python-httpx.org/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)

---

## 🎼 Orchestration

### Dagster
**Purpose**: Data orchestration platform for building data pipelines.

| Aspect | Details |
|--------|---------|
| **Why** | Modern, asset-centric, excellent observability, better DX than Airflow |
| **Use Case** | Schedule ingestion, coordinate dbt runs, monitor pipeline health |
| **Alternatives** | Apache Airflow, Prefect, Mage |

**Key Concepts**:
- **Assets**: Data artifacts (tables, files) that pipelines produce
- **Ops**: Individual computation units
- **Jobs**: Collections of ops that run together
- **Schedules**: Time-based triggers
- **Sensors**: Event-based triggers

**Learning Resources**:
- [Dagster Documentation](https://docs.dagster.io/)
- [Dagster University](https://courses.dagster.io/)

---

## 💎 Data Transformation

### dbt (Data Build Tool)
**Purpose**: Transform data in the warehouse using SQL with software engineering practices.

| Aspect | Details |
|--------|---------|
| **Why** | SQL-first, version controlled, testable, documentation built-in |
| **Use Case** | Implement Medallion Architecture (Bronze → Silver → Gold) |
| **Alternatives** | SQLMesh, custom SQL scripts |

**Medallion Architecture**:
```
Bronze (Raw)     → Silver (Cleaned)    → Gold (Business)
─────────────────────────────────────────────────────────
Raw API response → Typed, deduplicated → Aggregations,
                   validated data        KPIs, reports
```

### DuckDB
**Purpose**: In-process analytical database for local development.

| Aspect | Details |
|--------|---------|
| **Why** | Fast, zero dependencies, perfect for local dbt development |
| **Use Case** | Run dbt models locally before deploying to PostgreSQL |
| **Alternatives** | SQLite, local PostgreSQL |

**Learning Resources**:
- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Learn](https://courses.getdbt.com/)
- [DuckDB Documentation](https://duckdb.org/docs/)

---

## 🗄️ Storage

### PostgreSQL
**Purpose**: Primary relational database for storing weather data.

| Aspect | Details |
|--------|---------|
| **Why** | Robust, feature-rich, excellent for structured data |
| **Use Case** | Store Bronze/Silver/Gold tables |
| **Alternatives** | MySQL, SQLite |

**Learning Resources**:
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 📊 Visualization

### Apache Superset
**Purpose**: Modern data exploration and visualization platform.

| Aspect | Details |
|--------|---------|
| **Why** | Open source, feature-rich, integrates with many data sources |
| **Use Case** | Create dashboards for weather data visualization |
| **Alternatives** | Metabase, Grafana, Redash |

**Learning Resources**:
- [Superset Documentation](https://superset.apache.org/docs/intro)

---

## 📋 Data Governance

### DataHub
**Purpose**: Data catalog and metadata platform.

| Aspect | Details |
|--------|---------|
| **Why** | Open source, tracks data lineage, documents datasets |
| **Use Case** | Understand data flow, document schemas, track ownership |
| **Alternatives** | Apache Atlas, Amundsen, OpenMetadata |

**Learning Resources**:
- [DataHub Documentation](https://datahubproject.io/docs/)

---

## 🔄 CI/CD

### GitHub Actions
**Purpose**: Automate workflows directly in GitHub.

| Aspect | Details |
|--------|---------|
| **Why** | Native GitHub integration, free for public repos, extensive marketplace |
| **Use Case** | Linting, testing, Terraform validation, deployments |
| **Alternatives** | GitLab CI, Jenkins, CircleCI |

### Ruff
**Purpose**: Extremely fast Python linter and formatter.

| Aspect | Details |
|--------|---------|
| **Why** | 10-100x faster than alternatives, replaces multiple tools |
| **Use Case** | Lint Python code in CI pipeline |
| **Alternatives** | flake8, pylint, black |

**Learning Resources**:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

---

## 🔧 Development Tools

| Tool | Purpose |
|------|---------|
| **Make** | Task runner for common commands |
| **pre-commit** | Git hooks for code quality |
| **pytest** | Python testing framework |
| **Docker Compose** | Multi-container local development |

---

## 📚 Additional Learning Paths

### For DevOps Focus
1. Docker & Kubernetes fundamentals
2. Terraform for IaC
3. GitHub Actions for CI/CD
4. Monitoring with Prometheus/Grafana

### For Data Engineering Focus
1. Python data processing (Pydantic, HTTPX)
2. dbt for transformations
3. Dagster for orchestration
4. Data quality and testing

### For DataOps Focus
1. CI/CD for data pipelines
2. Data contracts and validation
3. Observability and monitoring
4. Data governance with DataHub
