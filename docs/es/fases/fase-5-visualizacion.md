# Fase 5: Visualización y Data Governance

## 🎯 Objetivo

Cerrar el círculo: mostrar el valor y asegurar el control. Desplegar herramientas de visualización e implementar data governance.

## 📊 Estado: 🔴 No Iniciada (0%)

### Pendiente
- [ ] Desplegar Apache Superset en Kubernetes
- [ ] Conectar Superset a PostgreSQL
- [ ] Crear dashboards meteorológicos
- [ ] Configurar DataHub para catálogo de datos
- [ ] Configurar tracking de linaje de datos
- [ ] Documentar datasets y ownership

## 🛠️ Herramientas Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| **Apache Superset** | BI y visualización de datos |
| **DataHub** | Catálogo de datos y linaje |
| **Kubernetes** | Orquestación de contenedores |

## 📁 Archivos Relevantes

```
weather-dataops-platform/
├── infra/
│   ├── superset.tf         # Deployment K8s de Superset
│   └── datahub.tf          # Deployment de DataHub
└── docs/
    └── dashboards/
        └── weather_overview.md  # Documentación de dashboards
```

## 📝 Pasos de Implementación

### Paso 1: Desplegar Superset en Kubernetes

**Opción A: Helm Chart (Recomendado)**
```bash
helm repo add superset https://apache.github.io/superset
helm install superset superset/superset \
  --namespace visualization \
  --create-namespace \
  --set service.type=NodePort \
  --set service.nodePort.http=30080
```

**Opción B: Terraform**
```hcl
# infra/superset.tf
resource "kubernetes_namespace" "visualization" {
  metadata {
    name = "visualization"
  }
}

resource "helm_release" "superset" {
  name       = "superset"
  repository = "https://apache.github.io/superset"
  chart      = "superset"
  namespace  = kubernetes_namespace.visualization.metadata[0].name

  set {
    name  = "service.type"
    value = "NodePort"
  }

  set {
    name  = "service.nodePort.http"
    value = "30080"
  }
}
```

### Paso 2: Configurar Conexión a Base de Datos

En la UI de Superset:
1. Ir a **Data** → **Databases** → **+ Database**
2. Seleccionar **PostgreSQL**
3. Configurar conexión:
   ```
   Host: postgres.database.svc.cluster.local
   Port: 5432
   Database: weather
   Username: weather_readonly
   Password: ****
   ```

### Paso 3: Crear Datasets

Registrar tablas Gold como datasets de Superset:
- `gold.fct_weather_daily`
- `gold.fct_weather_city_stats`

### Paso 4: Construir Dashboards

**Dashboard de Visión General del Clima**

| Gráfico | Tipo | Fuente de Datos |
|---------|------|-----------------|
| Tendencia de Temperatura | Líneas | fct_weather_daily |
| Comparación de Ciudades | Barras | fct_weather_city_stats |
| Condiciones Actuales | Big Number | Últimas observaciones |
| Mapa del Clima | Mapa | Coordenadas de ciudades |
| Heatmap de Humedad | Heatmap | fct_weather_daily |

**Ejemplo de Configuración de Gráfico**:
```sql
-- Tendencia de Temperatura por Ciudad
SELECT
    weather_date,
    city_name,
    avg_temperature_c
FROM gold.fct_weather_daily
WHERE weather_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY weather_date, city_name
```

### Paso 5: Desplegar DataHub

```bash
# Usando Docker Compose para desarrollo local
git clone https://github.com/datahub-project/datahub.git
cd datahub/docker
./quickstart.sh

# Acceder en http://localhost:9002
```

### Paso 6: Configurar Linaje de Datos

**Integración de dbt con DataHub**:
```bash
pip install acryl-datahub[dbt]

# Generar metadatos
datahub ingest -c dbt_recipe.yml
```

**Recipe de dbt**:
```yaml
# dbt_recipe.yml
source:
  type: dbt
  config:
    manifest_path: ./transformations/target/manifest.json
    catalog_path: ./transformations/target/catalog.json
    target_platform: postgres

sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
```

### Paso 7: Documentar Datasets

En DataHub, documentar cada dataset:
- **Descripción**: Qué representan los datos
- **Owner**: Equipo o persona responsable
- **Tags**: Categorías (ej. "weather", "gold", "daily")
- **Términos de Glosario**: Definiciones de negocio

## 📊 Ejemplos de Dashboard

### Visión General del Clima
```
┌─────────────────────────────────────────────────────────────────┐
│                 DASHBOARD VISIÓN GENERAL DEL CLIMA               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  Temp Actual     │  │  Humedad Media   │  │  Vel. Viento │  │
│  │     18.5°C       │  │      65%         │  │   12 km/h    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           Tendencia de Temperatura (Últimos 7 Días)         │ │
│  │  25°┤                                                       │ │
│  │  20°┤    ╭─╮   ╭───╮                                       │ │
│  │  15°┤───╯   ╰─╯     ╰───╮                                  │ │
│  │  10°┤                    ╰───                               │ │
│  │     └─────┬─────┬─────┬─────┬─────┬─────┬─────             │ │
│  │          Lun   Mar   Mié   Jue   Vie   Sáb   Dom           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │   Comparación Ciudades  │  │   Condiciones Climáticas    │  │
│  │   ████████ Madrid 22°   │  │   ☀️ Despejado: 45%         │  │
│  │   ██████ Barcelona 19°  │  │   ☁️ Nublado: 30%           │  │
│  │   █████ Londres 15°     │  │   🌧️ Lluvia: 25%            │  │
│  └─────────────────────────┘  └─────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔍 Vista de Linaje de Datos

```
┌─────────────────────────────────────────────────────────────────┐
│                      LINAJE DE DATOS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  OpenWeather API                                                 │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐                                                │
│  │ Python      │                                                │
│  │ Ingestor    │                                                │
│  └─────────────┘                                                │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Bronze:     │───▶│ Silver:     │───▶│ Gold:       │         │
│  │ weather_raw │    │ int_weather │    │ fct_daily   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                               │                  │
│                                               ▼                  │
│                                        ┌─────────────┐          │
│                                        │ Superset    │          │
│                                        │ Dashboard   │          │
│                                        └─────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## ✅ Checklist de Completado

- [ ] Superset desplegado y accesible
- [ ] Conexión a PostgreSQL configurada
- [ ] Tablas Gold registradas como datasets
- [ ] Al menos un dashboard creado
- [ ] DataHub desplegado
- [ ] Linaje de dbt importado
- [ ] Datasets documentados con owners
- [ ] Controles de acceso configurados

## 🔗 Recursos Relacionados

- [Documentación de Apache Superset](https://superset.apache.org/docs/intro)
- [Helm Chart de Superset](https://github.com/apache/superset/tree/master/helm/superset)
- [Documentación de DataHub](https://datahubproject.io/docs/)
- [Integración dbt con DataHub](https://datahubproject.io/docs/generated/ingestion/sources/dbt)

## 🎉 ¡Proyecto Completo!

Una vez completada esta fase, tienes una plataforma de datos totalmente funcional:

```
API → Ingestar → Almacenar → Transformar → Visualizar → Gobernar
```

### Próximos Pasos para Aprender
- Añadir más fuentes de datos
- Implementar streaming en tiempo real
- Configurar alertas y monitorización
- Explorar despliegue en cloud (AWS, GCP, Azure)
- Añadir capacidades de ML/AI
