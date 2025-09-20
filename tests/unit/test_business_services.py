import pytest
from jewelry_description.business.services import JewelryCostCalculator
from jewelry_description.models.entities import Material, WorkTime

def test_basic_cost_calculation():
    material = Material(name="Copper", unit_price=100.0, quantity=2.0)
    work_time = WorkTime(hours=1.5, hourly_rate=200.0)
    calculator = JewelryCostCalculator()
    cost = calculator.calculate([material], [], work_time)
    assert cost == pytest.approx(100.0 * 2.0 + 1.5 * 200.0)
