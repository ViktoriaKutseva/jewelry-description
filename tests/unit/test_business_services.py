from jewelry_description.business.services import JewelryCostCalculatorService
from jewelry_description.models.entities import (
    Material,
    WorkTime,
    JewelryCostInput,
    Consumable,
)


class TestJewelryCostCalculatorService:
    def test_calculate_cost_simple(self) -> None:
        service = JewelryCostCalculatorService()

        material = Material(name="Copper", unit_price=10.0, quantity=5.0)
        work_time = WorkTime(hours=2.0, hourly_rate=100.0)
        consumables = [Consumable(name="Polish", approx_cost=50.0)]

        input_data = JewelryCostInput(
            materials=[material], consumables=consumables, work_time=work_time
        )

        result = service.calculate_cost(input_data)

        assert (
            result.total_cost == 300.0
        )  # 50 (material) + 200 (work) + 50 (consumable)
        assert "Copper (5.0 г)" in result.cost_breakdown
        assert "Время (2.0 ч)" in result.cost_breakdown
        assert "Polish" in result.cost_breakdown

    def test_calculate_cost_with_defect(self) -> None:
        service = JewelryCostCalculatorService()

        material = Material(name="Copper", unit_price=10.0, quantity=5.0)
        work_time = WorkTime(hours=2.0, hourly_rate=100.0)

        input_data = JewelryCostInput(
            materials=[material],
            consumables=[],
            work_time=work_time,
            defect_percent=10.0,  # 10% defect
        )

        result = service.calculate_cost(input_data)

        expected_total = 275.0  # 250 base + 25 defect (10% of 250)

        assert result.total_cost == expected_total
        assert "Брак (10.0%)" in result.cost_breakdown
