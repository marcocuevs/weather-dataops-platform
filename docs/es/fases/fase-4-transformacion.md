# Fase 4: Transformación (La Refinería)

## 🎯 Objetivo

Convertir datos crudos en información útil para negocio usando dbt y el patrón Medallion Architecture.

## 📊 Estado: 🔴 No Iniciada (0%)

### Pendiente
- [ ] Configurar proyecto dbt
- [ ] Configurar DuckDB para desarrollo local
- [ ] Configurar PostgreSQL para producción
- [ ] Crear modelos Bronze (staging)
- [ ] Crear modelos Silver (limpios)
- [ ] Crear modelos Gold (negocio)
- [ ] Añadir tests de datos
- [ ] Generar documentación

## 🛠️ Herramientas Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| **dbt** | Transformaciones SQL con prácticas de ingeniería de software |
| **DuckDB** | Base de datos rápida para desarrollo local |
| **PostgreSQL** | Base de datos de producción |

## 📁 Archivos Relevantes

```
weather-dataops-platform/
└── transformations/
    ├── dbt_project.yml
    ├── profiles.yml
    ├── models/
    │   ├── bronze/
    │   │   ├── _bronze__models.yml
    │   │   └── stg_weather_raw.sql
    │   ├── silver/
    │   │   ├── _silver__models.yml
    │   │   ├── int_weather_cleaned.sql
    │   │   └── int_weather_hourly.sql
    │   └── gold/
    │       ├── _gold__models.yml
    │       ├── fct_weather_daily.sql
    │       └── fct_weather_city_stats.sql
    ├── tests/
    │   └── generic/
    ├── macros/
    └── seeds/
```

## 🏗️ Medallion Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEDALLION ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │  BRONZE  │ ───▶ │  SILVER  │ ───▶ │   GOLD   │              │
│  │   Raw    │      │  Limpio  │      │ Negocio  │              │
│  └──────────┘      └──────────┘      └──────────┘              │
│                                                                  │
│  • Datos crudos    • Columnas        • Agregaciones             │
│    de API            tipadas         • KPIs                     │
│  • Tal cual del    • Deduplicados    • Listo para BI            │
│    origen          • Validados       • Lógica de                │
│  • Solo append     • Estandarizados    negocio                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📝 Pasos de Implementación

### Paso 1: Inicializar Proyecto dbt

```bash
cd transformations
pip install dbt-core dbt-duckdb dbt-postgres
dbt init weather_transforms
```

### Paso 2: Configurar Profiles

```yaml
# transformations/profiles.yml
weather_transforms:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ./dev.duckdb
      threads: 4
    
    prod:
      type: postgres
      host: "{{ env_var('POSTGRES_HOST') }}"
      port: 5432
      user: "{{ env_var('POSTGRES_USER') }}"
      password: "{{ env_var('POSTGRES_PASSWORD') }}"
      dbname: weather
      schema: analytics
      threads: 4
```

### Paso 3: Capa Bronze (Staging)

```sql
-- models/bronze/stg_weather_raw.sql
{{
    config(
        materialized='view',
        schema='bronze'
    )
}}

with source as (
    select * from {{ source('raw', 'weather_raw') }}
),

staged as (
    select
        id,
        city_name,
        country_code,
        latitude,
        longitude,
        temperature_kelvin,
        feels_like_kelvin,
        humidity_percent,
        pressure_hpa,
        wind_speed_ms,
        wind_direction_deg,
        weather_condition,
        weather_description,
        cloudiness_percent,
        visibility_meters,
        recorded_at,
        ingested_at,
        _loaded_at
    from source
)

select * from staged
```

### Paso 4: Capa Silver (Limpio)

```sql
-- models/silver/int_weather_cleaned.sql
{{
    config(
        materialized='incremental',
        schema='silver',
        unique_key='record_id'
    )
}}

with bronze as (
    select * from {{ ref('stg_weather_raw') }}
),

cleaned as (
    select
        {{ dbt_utils.generate_surrogate_key(['city_name', 'recorded_at']) }} as record_id,
        city_name,
        country_code,
        latitude,
        longitude,
        
        -- Convertir Kelvin a Celsius
        round(temperature_kelvin - 273.15, 2) as temperature_celsius,
        round(feels_like_kelvin - 273.15, 2) as feels_like_celsius,
        
        humidity_percent,
        pressure_hpa,
        
        -- Convertir m/s a km/h
        round(wind_speed_ms * 3.6, 2) as wind_speed_kmh,
        wind_direction_deg,
        
        weather_condition,
        weather_description,
        cloudiness_percent,
        
        -- Convertir metros a kilómetros
        round(visibility_meters / 1000.0, 2) as visibility_km,
        
        recorded_at,
        ingested_at,
        current_timestamp as transformed_at
        
    from bronze
    where city_name is not null
      and temperature_kelvin between 200 and 350  -- Rango válido de temperatura
)

select * from cleaned

{% if is_incremental() %}
where recorded_at > (select max(recorded_at) from {{ this }})
{% endif %}
```

### Paso 5: Capa Gold (Negocio)

```sql
-- models/gold/fct_weather_daily.sql
{{
    config(
        materialized='table',
        schema='gold'
    )
}}

with silver as (
    select * from {{ ref('int_weather_cleaned') }}
),

daily_aggregates as (
    select
        city_name,
        country_code,
        date_trunc('day', recorded_at) as weather_date,
        
        -- Métricas de temperatura
        round(avg(temperature_celsius), 2) as avg_temperature_c,
        round(min(temperature_celsius), 2) as min_temperature_c,
        round(max(temperature_celsius), 2) as max_temperature_c,
        
        -- Métricas de humedad
        round(avg(humidity_percent), 1) as avg_humidity_pct,
        
        -- Métricas de viento
        round(avg(wind_speed_kmh), 2) as avg_wind_speed_kmh,
        round(max(wind_speed_kmh), 2) as max_wind_speed_kmh,
        
        -- Conteos
        count(*) as observation_count,
        
        -- Condición meteorológica más común
        mode() within group (order by weather_condition) as dominant_weather,
        
        max(transformed_at) as last_updated
        
    from silver
    group by 1, 2, 3
)

select * from daily_aggregates
```

### Paso 6: Añadir Tests de Datos

```yaml
# models/silver/_silver__models.yml
version: 2

models:
  - name: int_weather_cleaned
    description: "Observaciones meteorológicas limpias y tipadas"
    columns:
      - name: record_id
        description: "Identificador único para cada observación"
        tests:
          - unique
          - not_null
      
      - name: temperature_celsius
        description: "Temperatura en Celsius"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: -50
              max_value: 60
      
      - name: humidity_percent
        description: "Porcentaje de humedad relativa"
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100
```

### Paso 7: Ejecutar dbt

```bash
# Ejecutar todos los modelos
dbt run

# Ejecutar tests
dbt test

# Generar documentación
dbt docs generate
dbt docs serve
```

## 🔄 Estrategia Dual Stack

| Entorno | Base de Datos | Propósito |
|---------|---------------|-----------|
| **Dev Local** | DuckDB | Iteración rápida, sin setup |
| **CI/CD** | DuckDB | Ejecución rápida de tests en pipeline |
| **Producción** | PostgreSQL | Datos reales, almacenamiento persistente |
| **Futuro** | Databricks | Simulación de escala enterprise |

## ✅ Checklist de Completado

- [ ] Proyecto dbt inicializado
- [ ] Profiles configurados para DuckDB y PostgreSQL
- [ ] Modelos Bronze creados (staging)
- [ ] Modelos Silver creados (limpios, tipados)
- [ ] Modelos Gold creados (agregaciones)
- [ ] Tests de datos pasando
- [ ] Documentación generada
- [ ] Pipeline CI ejecuta tests de dbt

## 🔗 Recursos Relacionados

- [Documentación de dbt](https://docs.getdbt.com/)
- [Mejores Prácticas de dbt](https://docs.getdbt.com/guides/best-practices)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [Paquete dbt-utils](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)

## ➡️ Siguiente Fase

Una vez las transformaciones funcionen, proceder a [Fase 5: Visualización](./fase-5-visualizacion.md)
