# Phase 4: Transformation (The Refinery)

## 🎯 Objective

Convert raw data into useful business information using dbt and the Medallion Architecture pattern.

## 📊 Status: 🔴 Not Started (0%)

### Pending
- [ ] Set up dbt project
- [ ] Configure DuckDB for local development
- [ ] Configure PostgreSQL for production
- [ ] Create Bronze models (staging)
- [ ] Create Silver models (cleaned)
- [ ] Create Gold models (business)
- [ ] Add data tests
- [ ] Generate documentation

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **dbt** | SQL transformations with software engineering practices |
| **DuckDB** | Fast local development database |
| **PostgreSQL** | Production database |

## 📁 Relevant Files

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
│  │   Raw    │      │  Cleaned │      │ Business │              │
│  └──────────┘      └──────────┘      └──────────┘              │
│                                                                  │
│  • Raw API data    • Typed columns   • Aggregations             │
│  • As-is from      • Deduplicated    • KPIs                     │
│    source          • Validated       • Ready for BI             │
│  • Append-only     • Standardized    • Business logic           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 📝 Implementation Steps

### Step 1: Initialize dbt Project

```bash
cd transformations
pip install dbt-core dbt-duckdb dbt-postgres
dbt init weather_transforms
```

### Step 2: Configure Profiles

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

### Step 3: Bronze Layer (Staging)

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

### Step 4: Silver Layer (Cleaned)

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
        
        -- Convert Kelvin to Celsius
        round(temperature_kelvin - 273.15, 2) as temperature_celsius,
        round(feels_like_kelvin - 273.15, 2) as feels_like_celsius,
        
        humidity_percent,
        pressure_hpa,
        
        -- Convert m/s to km/h
        round(wind_speed_ms * 3.6, 2) as wind_speed_kmh,
        wind_direction_deg,
        
        weather_condition,
        weather_description,
        cloudiness_percent,
        
        -- Convert meters to kilometers
        round(visibility_meters / 1000.0, 2) as visibility_km,
        
        recorded_at,
        ingested_at,
        current_timestamp as transformed_at
        
    from bronze
    where city_name is not null
      and temperature_kelvin between 200 and 350  -- Valid temperature range
)

select * from cleaned

{% if is_incremental() %}
where recorded_at > (select max(recorded_at) from {{ this }})
{% endif %}
```

### Step 5: Gold Layer (Business)

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
        
        -- Temperature metrics
        round(avg(temperature_celsius), 2) as avg_temperature_c,
        round(min(temperature_celsius), 2) as min_temperature_c,
        round(max(temperature_celsius), 2) as max_temperature_c,
        
        -- Humidity metrics
        round(avg(humidity_percent), 1) as avg_humidity_pct,
        
        -- Wind metrics
        round(avg(wind_speed_kmh), 2) as avg_wind_speed_kmh,
        round(max(wind_speed_kmh), 2) as max_wind_speed_kmh,
        
        -- Counts
        count(*) as observation_count,
        
        -- Most common weather condition
        mode() within group (order by weather_condition) as dominant_weather,
        
        max(transformed_at) as last_updated
        
    from silver
    group by 1, 2, 3
)

select * from daily_aggregates
```

### Step 6: Add Data Tests

```yaml
# models/silver/_silver__models.yml
version: 2

models:
  - name: int_weather_cleaned
    description: "Cleaned and typed weather observations"
    columns:
      - name: record_id
        description: "Unique identifier for each observation"
        tests:
          - unique
          - not_null
      
      - name: temperature_celsius
        description: "Temperature in Celsius"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: -50
              max_value: 60
      
      - name: humidity_percent
        description: "Relative humidity percentage"
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100
```

### Step 7: Run dbt

```bash
# Run all models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

## 🔄 Dual Stack Strategy

| Environment | Database | Purpose |
|-------------|----------|---------|
| **Local Dev** | DuckDB | Fast iteration, no setup needed |
| **CI/CD** | DuckDB | Quick test runs in pipeline |
| **Production** | PostgreSQL | Real data, persistent storage |
| **Future** | Databricks | Enterprise scale simulation |

## ✅ Completion Checklist

- [ ] dbt project initialized
- [ ] Profiles configured for DuckDB and PostgreSQL
- [ ] Bronze models created (staging)
- [ ] Silver models created (cleaned, typed)
- [ ] Gold models created (aggregations)
- [ ] Data tests passing
- [ ] Documentation generated
- [ ] CI pipeline runs dbt tests

## 🔗 Related Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Medallion Architecture](https://www.databricks.com/glossary/medallion-architecture)
- [dbt-utils Package](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)

## ➡️ Next Phase

Once transformations are working, proceed to [Phase 5: Visualization](./phase-5-visualization.md)
