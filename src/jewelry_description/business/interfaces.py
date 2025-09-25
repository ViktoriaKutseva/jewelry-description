from typing import Protocol, List, Dict, Optional
from jewelry_description.models.entities import Material, Consumable, WorkTime


class CostCalculator(Protocol):
    def calculate(
        self, 
        materials: List[Material], 
        consumables: List[Consumable], 
        work_time: WorkTime, 
        **kwargs
    ) -> float:
        ...


class MaterialRepository(Protocol):
    """Protocol for material data access."""
    
    async def get_all(self) -> List[Dict[str, any]]:
        """Get all materials."""
        ...
    
    async def add(self, name: str, price: float, unit: str, category: str) -> bool:
        """Add a new material."""
        ...
    
    async def find_by_name(self, name: str) -> Optional[Dict[str, any]]:
        """Find material by name."""
        ...


class DescriptionGenerator(Protocol):
    """Protocol for generating jewelry descriptions."""
    
    def generate(self, jewelry_type: str, materials: List[Dict[str, any]]) -> str:
        """Generate mystical jewelry description."""
        ...
