# Multi-stage Dockerfile for production deployment
# Stage 1: Build stage
FROM python:3.12-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY src/ ./src/

# Stage 2: Runtime stage
FROM python:3.12-slim as runtime

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src/ ./src/

# Copy static files and templates
COPY --chown=app:app src/jewelry_description/entrypoints/web/static ./static
COPY --chown=app:app src/jewelry_description/entrypoints/web/templates ./templates

# Make sure scripts are executable
RUN chmod +x /app/.venv/bin/*

# Switch to non-root user
USER app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV JEWELRY_ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "jewelry_description.entrypoints.web.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]