"""
Dependency injection configuration for the web application.
"""

from jewelry_description.business.interfaces import IMaterialRepository, IJewelryCostCalculator, IDescriptionGenerator
from jewelry_description.integrations.database.repositories import CsvMaterialRepository
from jewelry_description.business.services import WebJewelryCostCalculatorService, JewelryDescriptionGeneratorService


def get_material_repository() -> IMaterialRepository:
    """Create and return material repository instance."""
    return CsvMaterialRepository()


def get_cost_calculator() -> IJewelryCostCalculator:
    """Create and return cost calculator service instance."""
    material_repo = get_material_repository()
    return WebJewelryCostCalculatorService(material_repo)


def get_description_generator() -> IDescriptionGenerator:
    """Create and return description generator instance."""
    return JewelryDescriptionGeneratorService()