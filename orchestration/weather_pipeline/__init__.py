# =============================================================================
# Dagster Definitions - Entry point for Dagster
# This file tells Dagster what assets, jobs, and schedules are available
# =============================================================================

from dagster import Definitions

from .assets import raw_weather_data

# Definitions: the main entry point for Dagster
# Similar to how Azure Data Factory has a "pipeline" as entry point
defs = Definitions(
    assets=[raw_weather_data],
)
