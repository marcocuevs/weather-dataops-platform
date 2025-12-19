-- =============================================================================
-- Mart Model: weather_summary
-- Aggregated weather data ready for dashboards
-- =============================================================================

WITH staged_weather AS (
    SELECT * FROM {{ ref('stg_weather') }}
)

SELECT
    city_name,
    country_code,
    
    -- Latest values
    temp_celsius,
    feels_like_celsius,
    humidity_percent,
    weather_condition,
    weather_description,
    
    -- Categorization
    CASE
        WHEN temp_celsius < 0 THEN 'Freezing'
        WHEN temp_celsius < 10 THEN 'Cold'
        WHEN temp_celsius < 20 THEN 'Mild'
        WHEN temp_celsius < 30 THEN 'Warm'
        ELSE 'Hot'
    END AS temp_category,
    
    CASE
        WHEN humidity_percent < 30 THEN 'Low'
        WHEN humidity_percent < 60 THEN 'Normal'
        ELSE 'High'
    END AS humidity_category,
    
    -- Metadata
    measurement_timestamp,
    loaded_at

FROM staged_weather
