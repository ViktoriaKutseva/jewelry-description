from typing import List
from ..models.entities import JewelryCostInput, JewelryCostResult, Material
from ..models.exceptions import CalculationError
from .interfaces import IJewelryCostCalculator, IMaterialRepository, IDescriptionGenerator


class JewelryCostCalculatorService(IJewelryCostCalculator):
    """Implementation of JewelryCostCalculator."""

    def calculate_cost(self, data: JewelryCostInput) -> JewelryCostResult:
        """Calculate jewelry cost with breakdown."""
        try:
            breakdown = {}
            total = 0.0

            # Materials
            for material in data.materials:
                cost = material.cost()
                breakdown[f"{material.name} ({material.quantity} {material.unit})"] = (
                    cost
                )
                total += cost

            # Work time
            work_cost = data.work_time.cost()
            breakdown[f"Время ({data.work_time.hours} ч)"] = work_cost
            total += work_cost

            # Consumables
            for consumable in data.consumables:
                breakdown[consumable.name] = consumable.approx_cost
                total += consumable.approx_cost

            # Additional costs
            if data.electricity_cost:
                breakdown["Электричество"] = data.electricity_cost
                total += data.electricity_cost

            if data.tool_depreciation:
                breakdown["Амортизация инструмента"] = data.tool_depreciation
                total += data.tool_depreciation

            if data.packaging_cost:
                breakdown["Упаковка"] = data.packaging_cost
                total += data.packaging_cost

            # Extra costs
            for extra in data.extra_costs:
                breakdown[extra.name] = extra.approx_cost
                total += extra.approx_cost

            # Defect percentage
            if data.defect_percent:
                defect_cost = total * data.defect_percent / 100
                breakdown[f"Брак ({data.defect_percent}%)"] = defect_cost
                total += defect_cost

            # Recommended prices
            min_price = total * 2
            comfort_price = total * 2.5
            premium_price = total * 3
            recommended = {
                "Минимальная (×2)": min_price,
                "Комфортная (×2.5)": comfort_price,
                "Премиум (×3)": premium_price,
            }

            comment = (
                f"👉 Отличная розничная цена: от {int(min_price * 1.1)} "
                f"до {int(comfort_price * 1.1)} тг, в зависимости от упаковки и позиционирования."
            )

            return JewelryCostResult(
                cost_breakdown=breakdown,
                total_cost=total,
                recommended_prices=recommended,
                price_comment=comment,
            )

        except Exception as e:
            raise CalculationError(f"Error calculating jewelry cost: {e}") from e


class WebJewelryCostCalculatorService(IJewelryCostCalculator):
    """Web-specific jewelry cost calculator with enhanced features."""

    def __init__(self, material_repo: IMaterialRepository):
        self._material_repo = material_repo

    def calculate_cost(self, data: JewelryCostInput) -> JewelryCostResult:
        """Calculate jewelry cost with enhanced web features."""
        # For now, delegate to the base implementation
        # In the future, this could include web-specific logic like
        # material validation against repository, caching, etc.
        base_calculator = JewelryCostCalculatorService()
        return base_calculator.calculate_cost(data)


class JewelryDescriptionGeneratorService(IDescriptionGenerator):
    """Service for generating jewelry descriptions."""

    def generate_description(self, jewelry_type: str, materials: List[Material]) -> str:
        """Generate a mystical jewelry description."""
        # Basic implementation - can be enhanced later
        material_names = [m.name for m in materials]
        materials_text = ", ".join(material_names)

        descriptions = {
            "ring": f"Кольцо из {materials_text} - символ вечной любви и гармонии.",
            "necklace": f"Кулон из {materials_text} - талисман защиты и мудрости.",
            "bracelet": f"Браслет из {materials_text} - оберег силы и процветания.",
            "earrings": f"Серьги из {materials_text} - украшение грации и элегантности.",
        }

        return descriptions.get(jewelry_type.lower(), f"Украшение из {materials_text} - произведение искусства.")
