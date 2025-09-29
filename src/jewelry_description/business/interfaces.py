from typing import Protocol, List, Optional
from ..models.entities import Material, JewelryCostInput, JewelryCostResult


class IMaterialRepository(Protocol):
    """Interface for material data access."""

    def load_materials_from_csv(self, csv_path: str = "old_data/info.csv") -> List[Material]: ...

    def find_material_by_name(self, name: str) -> Optional[Material]: ...

    def get_filtered_materials(self, csv_path: str = "old_data/info.csv") -> List[Material]: ...


class IJewelryCostCalculator(Protocol):
    """Interface for jewelry cost calculation."""

    def calculate_cost(self, data: JewelryCostInput) -> JewelryCostResult: ...


class IDescriptionGenerator(Protocol):
    """Interface for jewelry description generation."""

    def generate_description(self, jewelry_type: str, materials: List[Material]) -> str: ...
