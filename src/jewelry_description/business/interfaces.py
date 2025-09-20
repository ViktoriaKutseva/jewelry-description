from typing import Protocol
from src.jewelry_description.models.entities import Material, Consumable, WorkTime

class CostCalculator(Protocol):
    def calculate(self, materials: list[Material], consumables: list[Consumable], work_time: WorkTime, **kwargs) -> float:
        ...
