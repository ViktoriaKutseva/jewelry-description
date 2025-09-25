"""
Dependency injection for the web API.
"""
from jewelry_description.business.services import JewelryCostCalculator, WebJewelryCostService
from jewelry_description.business.description_service import JewelryDescriptionService
from jewelry_description.integrations.database.repositories import MaterialSQLiteRepository
from jewelry_description.business.interfaces import MaterialRepository, DescriptionGenerator


def create_material_repository() -> MaterialRepository:
    """Create material repository instance."""
    return MaterialSQLiteRepository()


def create_description_generator() -> DescriptionGenerator:
    """Create description generator instance."""
    return JewelryDescriptionService()


def create_cost_calculator() -> JewelryCostCalculator:
    """Create cost calculator instance."""
    return JewelryCostCalculator()


def create_web_cost_service() -> WebJewelryCostService:
    """Create web cost service with dependencies."""
    calculator = create_cost_calculator()
    return WebJewelryCostService(calculator)