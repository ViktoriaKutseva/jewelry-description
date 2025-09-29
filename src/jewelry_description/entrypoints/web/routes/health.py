"""
Health check endpoints.
"""

from datetime import datetime
from fastapi import APIRouter
from loguru import logger

from ..schemas import HealthCheckResponse


router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns the current status of the application and its services.
    """
    try:
        # Check if we can access our services
        services_status = {}

        try:
            from ..dependencies import get_material_repository
            repo = get_material_repository()
            # Try to load materials to verify repository works
            _ = repo.load_materials_from_csv()  # Test repository functionality
            services_status["material_repository"] = "healthy"
        except Exception as e:
            logger.warning("Material repository health check failed", error=str(e))
            services_status["material_repository"] = "unhealthy"

        try:
            from ..dependencies import get_cost_calculator
            _ = get_cost_calculator()  # Test calculator instantiation
            services_status["cost_calculator"] = "healthy"
        except Exception as e:
            logger.warning("Cost calculator health check failed", error=str(e))
            services_status["cost_calculator"] = "unhealthy"

        try:
            from ..dependencies import get_description_generator
            _ = get_description_generator()  # Test generator instantiation
            services_status["description_generator"] = "healthy"
        except Exception as e:
            logger.warning("Description generator health check failed", error=str(e))
            services_status["description_generator"] = "unhealthy"

        # Get version from settings
        try:
            from jewelry_description.config.settings import settings
            version = settings.version
        except Exception:
            version = "unknown"

        response = HealthCheckResponse(
            status="healthy" if all(s == "healthy" for s in services_status.values()) else "degraded",
            version=version,
            timestamp=datetime.now().isoformat(),
            services=services_status,
        )

        logger.debug("Health check completed", status=response.status)
        return response

    except Exception as e:
        logger.error("Health check failed", error=str(e))
        # Return unhealthy status if health check itself fails
        return HealthCheckResponse(
            status="unhealthy",
            version="unknown",
            timestamp=datetime.now().isoformat(),
            services={"health_check": "failed"}
        )