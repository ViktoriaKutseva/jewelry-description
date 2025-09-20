import pytest
from fastapi.testclient import TestClient
from src.jewelry_description.entrypoints.api.main import app
from src.jewelry_description.models.entities import CalculationInput, CalculationResult, Material, Consumable, WorkTime, JewelryMeta
from src.jewelry_description.business.services import calculate_jewelry_price

client = TestClient(app)

# ...existing tests...

def test_calculation_adapter():
    # Prepare sample input
    input_data = CalculationInput(
        materials=[Material(name="Gold", unit_price=4200, quantity=0.5, unit="g")],
        consumables=[Consumable(name="Consumables", approx_cost=350)],
        work_time=WorkTime(hours=2.5, hourly_rate=2500),
        electricity_cost=0,
        tool_depreciation=0,
        packaging_cost=0,
        defect_percent=0,
        jewelry_meta=JewelryMeta(type="bracelet", size="18 cm", style="boho", features="gift", photo_url="")
    )
    # Call business logic
    result = calculate_jewelry_price(input_data)
    assert isinstance(result, CalculationResult)
    assert result.total_cost > 0
    assert result.recommended_price > result.total_cost
    assert "bracelet" in result.instagram_description

def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text

def test_get_materials():
    response = client.get("/api/materials")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_calculate():
    payload = {
        "materials": [{"name": "Gold", "unit_price": 4200, "quantity": 0.5, "unit": "g"}],
        "consumables": [{"name":"Consumables", "approx_cost":350}],
        "work_time": {"hours": 2.5, "hourly_rate": 2500},
        "electricity_cost": 0,
        "tool_depreciation": 0,
        "packaging_cost": 0,
        "defect_percent": 0,
        "jewelry_meta": {"type":"bracelet","size":"18 cm","style":"boho","features":"gift","photo_url":""}
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "total_cost" in data
    assert "recommended_price" in data

def test_post_export_md():
    payload = {
        "materials": [{"name": "Gold", "unit_price": 4200, "quantity": 0.5, "unit": "g"}],
        "consumables": [{"name":"Consumables", "approx_cost":350}],
        "work_time": {"hours": 2.5, "hourly_rate": 2500},
        "electricity_cost": 0,
        "tool_depreciation": 0,
        "packaging_cost": 0,
        "defect_percent": 0,
        "jewelry_meta": {"type":"bracelet","size":"18 cm","style":"boho","features":"gift","photo_url":""}
    }
    response = client.post("/api/export_md", json=payload)
    assert response.status_code == 200
    assert "# Jewelry Description" in response.text