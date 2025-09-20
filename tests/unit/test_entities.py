from jewelry_description.models.entities import Material, WorkTime

def test_material_cost():
    m = Material(name="Silver", unit_price=50.0, quantity=3.0)
    assert m.cost() == 150.0

def test_work_time_cost():
    w = WorkTime(hours=2.0, hourly_rate=120.0)
    assert w.cost() == 240.0
