"""
Pydantic request models for API endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class MaterialItem(BaseModel):
    """Material item for cost calculation."""
    name: str = Field(..., min_length=1, max_length=100)
    unit_price: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    unit: str = Field(default="г", max_length=10)


class ConsumableItem(BaseModel):
    """Consumable item for cost calculation."""
    name: str = Field(..., min_length=1, max_length=100)
    approx_cost: float = Field(..., gt=0)


class ExtraCostItem(BaseModel):
    """Extra cost item for cost calculation."""
    name: str = Field(..., min_length=1, max_length=100)
    approx_cost: float = Field(..., gt=0)


class CalculateCostRequest(BaseModel):
    """Request model for cost calculation."""
    materials: List[MaterialItem] = Field(..., min_items=1)
    jewelry_type: str = Field(..., min_length=1, max_length=50)
    weight: float = Field(..., gt=0)
    labor_cost: float = Field(..., ge=0)
    markup: float = Field(..., ge=0)
    complexity: str = Field(default="medium")
    quality: str = Field(default="premium")
    include_gemstones: bool = Field(default=False)
    include_findings: bool = Field(default=False)


class AddMaterialRequest(BaseModel):
    """Request model for adding a custom material."""
    name: str = Field(..., min_length=1, max_length=100)
    unit_price: float = Field(..., gt=0)
    unit: str = Field(default="г", max_length=10)
    category: str = Field(default="material", max_length=20)

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str) -> str:
        """Validate unit is either 'г' or 'шт'."""
        if v not in ["г", "шт"]:
            raise ValueError("Unit must be either 'г' (grams) or 'шт' (pieces)")
        return v


class UpdateMaterialRequest(BaseModel):
    """Request model for updating a material."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    unit_price: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = Field(None, max_length=10)
    category: Optional[str] = Field(None, max_length=20)

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str) -> str:
        """Validate unit is either 'г' or 'шт'."""
        if v not in ["г", "шт"]:
            raise ValueError("Unit must be either 'г' (grams) or 'шт' (pieces)")
        return v


class GenerateDescriptionRequest(BaseModel):
    """Request model for description generation."""
    jewelry_type: str = Field(..., min_length=1, max_length=50)
    materials: List[str] = Field(..., min_items=1, max_length=10)

    @field_validator("jewelry_type")
    @classmethod
    def validate_jewelry_type(cls, v: str) -> str:
        """Validate jewelry type is one of the supported types."""
        valid_types = ["ring", "necklace", "bracelet", "earrings", "choker", "pendant", "brooch"]
        if v.lower() not in valid_types:
            raise ValueError(f"Jewelry type must be one of: {', '.join(valid_types)}")
        return v.lower()