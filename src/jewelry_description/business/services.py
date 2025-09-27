from ..models.entities import JewelryCostInput, JewelryCostResult
from ..models.exceptions import CalculationError


class JewelryCostCalculatorService:
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
