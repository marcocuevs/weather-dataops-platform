🗺️ Master Plan: Weather DataOps Platform
Este documento detalla las fases de ejecución del proyecto, desde la base de infraestructura hasta la entrega de valor en dashboards.

🎯 Objetivo
Construir una plataforma de datos clonable y automatizada que extraiga información de una API meteorológica, la procese con estándares de ingeniería de software y la visualice, todo orquestado bajo principios DevOps.

🛠️ Fase 1: Cimientos e Infraestructura (En curso)
El objetivo es preparar el "escenario" donde correrá nuestro código.

Estructura Monorepo: Organización de carpetas para separar responsabilidades (Infra, Ingestión, Transformación).

Git & CI inicial: Configuración de .gitignore y GitHub Actions para validar la calidad del código (Linting con Ruff y validación de Terraform).

Infraestructura como Código (IaC): Uso de Terraform para levantar un clúster de Kubernetes (Kind) y una base de datos PostgreSQL local en Windows.

🐍 Fase 2: Ingestión "Pythonic" y Contenerización
Aquí aplicamos ingeniería de software pura al flujo de datos.

Contratos de Datos: Definición de modelos de datos con Pydantic V2 para asegurar la calidad desde el origen.

Cliente de API Robusto: Desarrollo de un cliente asíncrono (HTTPX) con manejo de errores, reintentos y logs profesionales.

Dockerización: Creación de Dockerfiles para empaquetar el ingestor como una unidad ejecutable e independiente.

Secrets Management: Gestión de API Keys mediante variables de entorno y secretos de GitHub.

🎼 Fase 3: Orquestación y Almacenamiento
El momento de unir las piezas y darles un orden lógico.

Despliegue en K8s: Desplegar nuestra base de datos y nuestro ingestor dentro del clúster local usando Terraform/Kubectl.

Orquestación con Dagster: Configurar Dagster como el "cerebro" que coordina cuándo se dispara la ingesta y verifica que los datos se han guardado correctamente.

Observabilidad: Implementar logs y alertas básicas para saber si la tubería de datos falla.

💎 Fase 4: Transformación (La Refinería)
Convertimos datos crudos en información útil para negocio.

dbt (Data Build Tool): Implementación de transformaciones SQL siguiendo el patrón Medallion Architecture:

Bronze: Datos crudos (Raw).

Silver: Datos limpios y tipados.

Gold: Tablas finales listas para análisis (ej. promedios móviles de temperatura).

Dual Stack: * Pruebas locales rápidas con DuckDB.

Simulación de entorno corporativo con Databricks.

📊 Fase 5: Visualización y Data Governance
El cierre del círculo: mostrar el valor y asegurar el control.

BI con Apache Superset: Despliegue de Superset en Kubernetes y creación de dashboards para visualizar el clima en tiempo real.

Catálogo de Datos: Introducción a DataHub para ver el linaje de los datos (de dónde vienen y qué transformaciones han sufrido).

📈 Resumen del Flujo de Datos Final
API OpenWeather → Python Ingestor (K8s) → Postgres (Bronze) → dbt (Silver/Gold) → Apache Superset