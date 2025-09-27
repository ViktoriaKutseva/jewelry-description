from jewelry_description.models.entities import Material, WorkTime, JewelryCostInput


class TestMaterial:
    def test_material_creation(self) -> None:
        material = Material(name="Copper", unit_price=10.0, quantity=5.0, unit="г")
        assert material.name == "Copper"
        assert material.unit_price == 10.0
        assert material.quantity == 5.0
        assert material.unit == "г"

    def test_material_cost_calculation(self) -> None:
        material = Material(name="Copper", unit_price=10.0, quantity=5.0, unit="г")
        assert material.cost() == 50.0


class TestWorkTime:
    def test_work_time_creation(self) -> None:
        work_time = WorkTime(hours=2.0, hourly_rate=100.0)
        assert work_time.hours == 2.0
        assert work_time.hourly_rate == 100.0

    def test_work_time_cost_calculation(self) -> None:
        work_time = WorkTime(hours=2.0, hourly_rate=100.0)
        assert work_time.cost() == 200.0


class TestJewelryCostInput:
    def test_input_creation(self) -> None:
        material = Material(name="Copper", unit_price=10.0, quantity=5.0)
        work_time = WorkTime(hours=2.0, hourly_rate=100.0)

        input_data = JewelryCostInput(
            materials=[material], consumables=[], work_time=work_time
        )

        assert len(input_data.materials) == 1
        assert input_data.materials[0].name == "Copper"
        assert input_data.work_time.hours == 2.0
