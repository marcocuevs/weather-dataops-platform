# Guía de Herramientas

Referencia completa de todas las herramientas usadas en este proyecto, por qué fueron elegidas y recursos de aprendizaje.

## 🏗️ Infraestructura como Código (IaC)

### Terraform
**Propósito**: Provisionar y gestionar infraestructura de forma declarativa.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Estándar de la industria, agnóstico de cloud, excelente gestión de estado |
| **Caso de Uso** | Definir clúster Kind, PostgreSQL y todos los recursos K8s |
| **Alternativas** | Pulumi, CloudFormation, Ansible |

**Recursos de Aprendizaje**:
- [Documentación de Terraform](https://developer.hashicorp.com/terraform/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

## 🐳 Contenerización y Orquestación

### Docker
**Propósito**: Empaquetar aplicaciones en contenedores portables.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Estándar de contenerización, entornos reproducibles |
| **Caso de Uso** | Contenerizar ingestor Python, dbt y todos los servicios |
| **Alternativas** | Podman, containerd |

### Kind (Kubernetes in Docker)
**Propósito**: Ejecutar clústeres Kubernetes locales para desarrollo.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Ligero, perfecto para desarrollo local, replica K8s de producción |
| **Caso de Uso** | Clúster K8s local para desplegar todos los servicios |
| **Alternativas** | Minikube, k3s, Docker Desktop K8s |

**Recursos de Aprendizaje**:
- [Documentación de Docker](https://docs.docker.com/)
- [Kind Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

---

## 🐍 Ingestión de Datos

### Python 3.11+
**Propósito**: Lenguaje de programación principal para pipelines de datos.

### HTTPX
**Propósito**: Cliente HTTP asíncrono moderno para llamadas a APIs.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Soporte async, HTTP/2, mejor que requests para apps modernas |
| **Caso de Uso** | Llamar a la API de OpenWeather con reintentos y manejo de errores |
| **Alternativas** | aiohttp, requests |

### Pydantic V2
**Propósito**: Validación de datos y gestión de configuración usando type hints de Python.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Type safety, validación automática, excelente para contratos de datos |
| **Caso de Uso** | Definir y validar esquemas de respuesta de la API |
| **Alternativas** | dataclasses, attrs, marshmallow |

**Recursos de Aprendizaje**:
- [Documentación de HTTPX](https://www.python-httpx.org/)
- [Documentación de Pydantic V2](https://docs.pydantic.dev/latest/)

---

## 🎼 Orquestación

### Dagster
**Propósito**: Plataforma de orquestación de datos para construir pipelines.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Moderno, centrado en assets, excelente observabilidad, mejor DX que Airflow |
| **Caso de Uso** | Programar ingestión, coordinar ejecuciones de dbt, monitorear salud del pipeline |
| **Alternativas** | Apache Airflow, Prefect, Mage |

**Conceptos Clave**:
- **Assets**: Artefactos de datos (tablas, archivos) que producen los pipelines
- **Ops**: Unidades individuales de computación
- **Jobs**: Colecciones de ops que se ejecutan juntas
- **Schedules**: Disparadores basados en tiempo
- **Sensors**: Disparadores basados en eventos

**Recursos de Aprendizaje**:
- [Documentación de Dagster](https://docs.dagster.io/)
- [Dagster University](https://courses.dagster.io/)

---

## 💎 Transformación de Datos

### dbt (Data Build Tool)
**Propósito**: Transformar datos en el warehouse usando SQL con prácticas de ingeniería de software.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | SQL-first, versionado, testeable, documentación integrada |
| **Caso de Uso** | Implementar Medallion Architecture (Bronze → Silver → Gold) |
| **Alternativas** | SQLMesh, scripts SQL custom |

**Medallion Architecture**:
```
Bronze (Raw)     → Silver (Limpio)     → Gold (Negocio)
─────────────────────────────────────────────────────────
Respuesta cruda  → Datos tipados,      → Agregaciones,
de la API          deduplicados,         KPIs, reportes
                   validados
```

### DuckDB
**Propósito**: Base de datos analítica in-process para desarrollo local.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Rápido, sin dependencias, perfecto para desarrollo local con dbt |
| **Caso de Uso** | Ejecutar modelos dbt localmente antes de desplegar a PostgreSQL |
| **Alternativas** | SQLite, PostgreSQL local |

**Recursos de Aprendizaje**:
- [Documentación de dbt](https://docs.getdbt.com/)
- [dbt Learn](https://courses.getdbt.com/)
- [Documentación de DuckDB](https://duckdb.org/docs/)

---

## 🗄️ Almacenamiento

### PostgreSQL
**Propósito**: Base de datos relacional principal para almacenar datos meteorológicos.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Robusto, rico en funcionalidades, excelente para datos estructurados |
| **Caso de Uso** | Almacenar tablas Bronze/Silver/Gold |
| **Alternativas** | MySQL, SQLite |

**Recursos de Aprendizaje**:
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)

---

## 📊 Visualización

### Apache Superset
**Propósito**: Plataforma moderna de exploración y visualización de datos.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Open source, rico en funcionalidades, integra con muchas fuentes de datos |
| **Caso de Uso** | Crear dashboards para visualización de datos meteorológicos |
| **Alternativas** | Metabase, Grafana, Redash |

**Recursos de Aprendizaje**:
- [Documentación de Superset](https://superset.apache.org/docs/intro)

---

## 📋 Data Governance

### DataHub
**Propósito**: Catálogo de datos y plataforma de metadatos.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Open source, rastrea linaje de datos, documenta datasets |
| **Caso de Uso** | Entender flujo de datos, documentar esquemas, rastrear ownership |
| **Alternativas** | Apache Atlas, Amundsen, OpenMetadata |

**Recursos de Aprendizaje**:
- [Documentación de DataHub](https://datahubproject.io/docs/)

---

## 🔄 CI/CD

### GitHub Actions
**Propósito**: Automatizar workflows directamente en GitHub.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | Integración nativa con GitHub, gratis para repos públicos, marketplace extenso |
| **Caso de Uso** | Linting, testing, validación de Terraform, despliegues |
| **Alternativas** | GitLab CI, Jenkins, CircleCI |

### Ruff
**Propósito**: Linter y formateador de Python extremadamente rápido.

| Aspecto | Detalles |
|---------|----------|
| **Por qué** | 10-100x más rápido que alternativas, reemplaza múltiples herramientas |
| **Caso de Uso** | Lint de código Python en pipeline CI |
| **Alternativas** | flake8, pylint, black |

**Recursos de Aprendizaje**:
- [Documentación de GitHub Actions](https://docs.github.com/en/actions)
- [Documentación de Ruff](https://docs.astral.sh/ruff/)

---

## 🔧 Herramientas de Desarrollo

| Herramienta | Propósito |
|-------------|-----------|
| **Make** | Task runner para comandos comunes |
| **pre-commit** | Git hooks para calidad de código |
| **pytest** | Framework de testing para Python |
| **Docker Compose** | Desarrollo local multi-contenedor |

---

## 📚 Rutas de Aprendizaje Adicionales

### Enfoque DevOps
1. Fundamentos de Docker y Kubernetes
2. Terraform para IaC
3. GitHub Actions para CI/CD
4. Monitorización con Prometheus/Grafana

### Enfoque Data Engineering
1. Procesamiento de datos con Python (Pydantic, HTTPX)
2. dbt para transformaciones
3. Dagster para orquestación
4. Calidad de datos y testing

### Enfoque DataOps
1. CI/CD para pipelines de datos
2. Contratos de datos y validación
3. Observabilidad y monitorización
4. Data governance con DataHub
