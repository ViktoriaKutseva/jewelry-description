from dataclasses import dataclass


@dataclass
class Material:
    name: str
    unit_price: float
    quantity: float
    unit: str = "г"

    def cost(self) -> float:
        return self.unit_price * self.quantity

@dataclass
class Consumable:
    name: str
    approx_cost: float

@dataclass
class WorkTime:
    hours: float
    hourly_rate: float

    def cost(self) -> float:
        return self.hours * self.hourly_rate
