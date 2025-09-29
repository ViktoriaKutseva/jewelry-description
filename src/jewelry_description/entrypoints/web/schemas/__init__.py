"""
Pydantic schemas for API request/response models.
"""

from .requests import (
    MaterialItem,
    ConsumableItem,
    ExtraCostItem,
    CalculateCostRequest,
    AddMaterialRequest,
    UpdateMaterialRequest,
    GenerateDescriptionRequest,
)
from .responses import (
    MaterialResponse,
    PriceRecommendations,
    CalculationMetadata,
    CostCalculationResponse,
    DescriptionGenerationResponse,
    HealthCheckResponse,
    ErrorResponse,
    ValidationErrorResponse,
)

__all__ = [
    # Requests
    "MaterialItem",
    "ConsumableItem",
    "ExtraCostItem",
    "CalculateCostRequest",
    "AddMaterialRequest",
    "UpdateMaterialRequest",
    "GenerateDescriptionRequest",
    # Responses
    "MaterialResponse",
    "PriceRecommendations",
    "CalculationMetadata",
    "CostCalculationResponse",
    "DescriptionGenerationResponse",
    "HealthCheckResponse",
    "ErrorResponse",
    "ValidationErrorResponse",
]