"""
Pydantic response models for API endpoints.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class MaterialResponse(BaseModel):
    """Response model for material data."""
    name: str
    unit_price: float
    unit: str
    category: str = "material"


class PriceRecommendations(BaseModel):
    """Recommended selling prices."""
    minimum: float = Field(..., description="2x cost - minimum recommended price")
    comfort: float = Field(..., description="2.5x cost - comfortable price")
    premium: float = Field(..., description="3x cost - premium price")


class CalculationMetadata(BaseModel):
    """Metadata about the cost calculation."""
    material_count: int
    has_consumables: bool
    has_extra_costs: bool
    defect_percentage: Optional[float] = None
    calculation_timestamp: str


class CostCalculationResponse(BaseModel):
    """Response model for cost calculation."""
    total_cost: float = Field(..., gt=0)
    cost_breakdown: Dict[str, float]
    recommended_prices: PriceRecommendations
    price_comment: str
    calculation_metadata: CalculationMetadata


class DescriptionGenerationResponse(BaseModel):
    """Response model for description generation."""
    description: str
    jewelry_type: str
    material_count: int
    hashtags: List[str] = Field(default_factory=list)


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str = "healthy"
    version: str
    timestamp: str
    services: Dict[str, str] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str
    type: str
    timestamp: Optional[str] = None
    request_id: Optional[str] = None


class ValidationErrorDetail(BaseModel):
    """Individual validation error detail."""
    loc: List[str] = Field(..., description="Location of the validation error")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")
    input: Optional[str] = Field(None, description="Input value that caused the error")
    ctx: Optional[Dict[str, Any]] = Field(None, description="Error context")
    url: Optional[str] = Field(None, description="Documentation URL")


class ValidationErrorResponse(BaseModel):
    """Response model for validation errors."""
    detail: List[ValidationErrorDetail]
    type: str = "validation_error"
    timestamp: Optional[str] = None
    request_id: Optional[str] = None