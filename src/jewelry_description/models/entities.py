from pydantic import BaseModel
from typing import List, Optional

class Material(BaseModel):
    name: str
    unit_price: float
    quantity: float
    unit: str

class Consumable(BaseModel):
    name: str
    approx_cost: float

class WorkTime(BaseModel):
    hours: float
    hourly_rate: float

class JewelryMeta(BaseModel):
    type: str
    size: str
    style: str
    features: Optional[str] = None
    photo_url: Optional[str] = None

class CalculationInput(BaseModel):
    materials: List[Material]
    consumables: List[Consumable]
    work_time: WorkTime
    electricity_cost: float
    tool_depreciation: float
    packaging_cost: float
    defect_percent: float
    jewelry_meta: JewelryMeta

class CalculationResult(BaseModel):
    total_cost: float
    recommended_price: float
    price_comment: str
    instagram_description: str