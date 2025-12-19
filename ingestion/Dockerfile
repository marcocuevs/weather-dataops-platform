# =============================================================================
# Dockerfile for Weather Ingestion Service
# Multi-stage build for smaller final image
# =============================================================================

# Stage 1: Base image with Python
FROM python:3.11-slim as base

# Prevents Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Stage 2: Install dependencies
FROM base as dependencies

# Copy only requirements first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final image
FROM dependencies as final

# Copy source code
COPY src/ ./src/

# Set the Python path so imports work correctly
ENV PYTHONPATH=/app/src

# Default command - run the main script
CMD ["python", "-m", "src.main"]
