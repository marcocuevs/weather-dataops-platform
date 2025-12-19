-- =============================================================================
-- Staging Model: stg_weather
-- Cleans and standardizes raw weather data from the API
-- =============================================================================

WITH raw_weather AS (
    SELECT * FROM {{ source('raw', 'weather_data') }}
)

SELECT
    -- Location info
    name AS city_name,
    coord_lat AS latitude,
    coord_lon AS longitude,
    sys_country AS country_code,
    
    -- Temperature (convert from Kelvin to Celsius)
    main_temp - 273.15 AS temp_celsius,
    main_feels_like - 273.15 AS feels_like_celsius,
    main_temp_min - 273.15 AS temp_min_celsius,
    main_temp_max - 273.15 AS temp_max_celsius,
    
    -- Atmospheric conditions
    main_pressure AS pressure_hpa,
    main_humidity AS humidity_percent,
    
    -- Wind
    wind_speed AS wind_speed_ms,
    wind_deg AS wind_direction_deg,
    
    -- Clouds
    clouds_all AS cloudiness_percent,
    
    -- Weather description
    weather_main AS weather_condition,
    weather_description AS weather_description,
    
    -- Timestamps
    dt AS measurement_timestamp,
    timezone AS timezone_offset_seconds,
    
    -- Metadata
    CURRENT_TIMESTAMP AS loaded_at

FROM raw_weather
