from typing import Protocol, List, Optional
from ..models.entities import Material, JewelryCostInput, JewelryCostResult


class MaterialRepository(Protocol):
    """Interface for material data access."""

    def load_materials_from_csv(self, csv_path: str) -> List[Material]: ...

    def find_material_by_name(self, name: str) -> Optional[Material]: ...

    def get_filtered_materials(self, csv_path: str) -> List[Material]: ...


class JewelryCostCalculator(Protocol):
    """Interface for jewelry cost calculation."""

    def calculate_cost(self, data: JewelryCostInput) -> JewelryCostResult: ...
