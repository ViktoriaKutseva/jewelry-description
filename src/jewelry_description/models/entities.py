from pydantic import BaseModel, Field
from typing import List, Dict


class Material(BaseModel):
    name: str
    unit_price: float = Field(
        ..., gt=0, description="цена за единицу (грамм, штуку и т.д.)"
    )
    quantity: float = Field(..., ge=0, description="количество (граммы, штуки и т.д.)")
    unit: str = Field(default="г", description="единица измерения")

    def cost(self) -> float:
        return self.unit_price * self.quantity


class Consumable(BaseModel):
    name: str
    approx_cost: float = Field(..., ge=0)


class WorkTime(BaseModel):
    hours: float = Field(..., gt=0)
    hourly_rate: float = Field(..., gt=0)

    def cost(self) -> float:
        return self.hours * self.hourly_rate


class JewelryCostInput(BaseModel):
    materials: List[Material]
    consumables: List[Consumable]
    work_time: WorkTime
    electricity_cost: float = Field(default=0.0, ge=0)
    tool_depreciation: float = Field(default=0.0, ge=0)
    packaging_cost: float = Field(default=0.0, ge=0)
    extra_costs: List[Consumable] = Field(default_factory=list)
    defect_percent: float = Field(
        default=0.0, ge=0, le=100, description="процент на брак"
    )


class JewelryCostResult(BaseModel):
    cost_breakdown: Dict[str, float]
    total_cost: float
    recommended_prices: Dict[str, float]
    price_comment: str
