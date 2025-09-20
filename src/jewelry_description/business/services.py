from jewelry_description.models.entities import Material, Consumable, WorkTime
from typing import List

class JewelryCostCalculator:
    def calculate(self, materials: List[Material], consumables: List[Consumable], work_time: WorkTime, electricity_cost: float = 0.0, tool_depreciation: float = 0.0, packaging_cost: float = 0.0, extra_costs: List[Consumable] = None, defect_percent: float = 0.0) -> float:
        if extra_costs is None:
            extra_costs = []
        material_cost = sum(m.cost() for m in materials)
        consumable_cost = sum(c.approx_cost for c in consumables)
        extra_cost = sum(c.approx_cost for c in extra_costs)
        work_cost = work_time.cost()
        total = material_cost + consumable_cost + work_cost + electricity_cost + tool_depreciation + packaging_cost + extra_cost
        if defect_percent > 0:
            total *= (1 + defect_percent / 100)
        return total
