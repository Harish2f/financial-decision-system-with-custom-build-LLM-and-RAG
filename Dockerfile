# ---------------------------------------------------------
# Base image
# ---------------------------------------------------------
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------------------------------------------------------
# System dependencies
# ---------------------------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------
# Working directory
# ---------------------------------------------------------
WORKDIR /app

# ---------------------------------------------------------
# Install Python dependencies first (better Docker cache)
# ---------------------------------------------------------
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && update-ca-certificates

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------
# Copy application code
# ---------------------------------------------------------
COPY . .

# ---------------------------------------------------------
# Security: do NOT bake secrets into image
# ---------------------------------------------------------
# Database credentials must come from ENV variables
# These are injected by Kubernetes / GitHub Actions
#
# DB_HOST
# DB_PORT
# DB_NAME
# DB_USER
# DB_PASSWORD
# DB_SSLMODE
#

# ---------------------------------------------------------
# Airflow configuration
# ---------------------------------------------------------
ENV AIRFLOW_HOME=/app/airflow

# ---------------------------------------------------------
# Default command
# ---------------------------------------------------------
# We don't start Airflow here.
# AKS will run:
#   airflow scheduler
#   airflow webserver
#   airflow workers
#
# This container only provides the runtime.
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
CMD ["/app/docker-entrypoint.sh"]