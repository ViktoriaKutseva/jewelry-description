"""Integration tests for web API endpoints using real database."""
from fastapi.testclient import TestClient


class TestMaterialsAPIIntegration:
    """Integration tests for materials API endpoints."""

    def test_get_materials_integration(self, client: TestClient, mock_csv_file):
        """Test materials retrieval with real CSV data."""
        # This test uses the actual CSV file and repository
        response = client.get("/api/v1/materials/")

        assert response.status_code == 200
        data = response.json()

        # Should return materials from the mock CSV
        assert isinstance(data, list)
        assert len(data) > 0

        # Check structure of first material
        material = data[0]
        assert "name" in material
        assert "unit_price" in material
        assert "unit" in material
        assert "category" in material

    def test_get_materials_with_limit(self, client: TestClient, mock_csv_file):
        """Test materials retrieval with limit parameter."""
        response = client.get("/api/v1/materials/?limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2

    def test_search_materials_integration(self, client: TestClient, mock_csv_file):
        """Test material search with real data."""
        response = client.get("/api/v1/materials/search?q=Test")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        # Should find materials containing "Test" in the name
        for material in data:
            assert "test" in material["name"].lower()

    def test_add_material_integration(self, client: TestClient):
        """Test adding a custom material."""
        material_data = {
            "name": "Custom Gem",
            "unit_price": 100.0,
            "unit": "шт",
            "category": "gem"
        }

        response = client.post("/api/v1/materials/", json=material_data)

        assert response.status_code == 201
        data = response.json()

        assert data["name"] == "Custom Gem"
        assert data["unit_price"] == 100.0
        assert data["unit"] == "шт"
        assert data["category"] == "gem"


class TestCalculatorAPIIntegration:
    """Integration tests for calculator API endpoints."""

    def test_calculate_cost_integration(self, client: TestClient):
        """Test cost calculation with real calculator service."""
        calculation_data = {
            "materials": [
                {
                    "name": "Silver",
                    "unit_price": 25.0,
                    "quantity": 10.0,
                    "unit": "г"
                }
            ],
            "hours": 2.0,
            "hourly_rate": 150.0,
            "jewelry_type": "ring",
            "consumables": [
                {
                    "name": "Polish",
                    "approx_cost": 50.0
                }
            ]
        }

        response = client.post("/api/v1/calculator/calculate", json=calculation_data)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "total_cost" in data
        assert "cost_breakdown" in data
        assert "recommended_prices" in data
        assert "price_comment" in data
        assert "calculation_metadata" in data

        # Verify cost is reasonable
        assert data["total_cost"] > 0

        # Verify recommended prices are calculated
        prices = data["recommended_prices"]
        assert "minimum" in prices
        assert "comfort" in prices
        assert "premium" in prices

        # Verify minimum price is at least 2x cost
        assert prices["minimum"] >= data["total_cost"] * 2

    def test_calculate_cost_with_extra_costs(self, client: TestClient):
        """Test cost calculation with extra costs."""
        calculation_data = {
            "materials": [
                {
                    "name": "Gold",
                    "unit_price": 150.0,
                    "quantity": 5.0,
                    "unit": "г"
                }
            ],
            "hours": 3.0,
            "hourly_rate": 200.0,
            "jewelry_type": "necklace",
            "extra_costs": [
                {
                    "name": "Packaging",
                    "approx_cost": 100.0
                }
            ],
            "electricity_cost": 25.0,
            "tool_depreciation": 15.0
        }

        response = client.post("/api/v1/calculator/calculate", json=calculation_data)

        assert response.status_code == 200
        data = response.json()

        # Should include all the extra costs
        assert data["total_cost"] > 750.0  # Base cost should be higher with gold

        # Check metadata
        metadata = data["calculation_metadata"]
        assert metadata["has_extra_costs"] is True

    def test_calculate_cost_with_defect_percentage(self, client: TestClient):
        """Test cost calculation with defect percentage."""
        calculation_data = {
            "materials": [
                {
                    "name": "Copper",
                    "unit_price": 20.0,
                    "quantity": 15.0,
                    "unit": "г"
                }
            ],
            "hours": 1.5,
            "hourly_rate": 100.0,
            "jewelry_type": "bracelet",
            "defect_percent": 10.0
        }

        response = client.post("/api/v1/calculator/calculate", json=calculation_data)

        assert response.status_code == 200
        data = response.json()

        # Should include defect cost in breakdown
        breakdown = data["cost_breakdown"]
        assert any("Брак" in key for key in breakdown.keys())

        # Metadata should include defect percentage
        metadata = data["calculation_metadata"]
        assert metadata["defect_percentage"] == 10.0


class TestDescriptionsAPIIntegration:
    """Integration tests for descriptions API endpoints."""

    def test_generate_description_integration(self, client: TestClient):
        """Test description generation with real service."""
        description_data = {
            "jewelry_type": "ring",
            "materials": ["Silver", "Diamond"]
        }

        response = client.post("/api/v1/descriptions/generate", json=description_data)

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "description" in data
        assert "jewelry_type" in data
        assert "material_count" in data
        assert "hashtags" in data

        # Verify content
        assert data["jewelry_type"] == "ring"
        assert data["material_count"] == 2
        assert len(data["description"]) > 0
        assert isinstance(data["hashtags"], list)
        assert len(data["hashtags"]) > 0

    def test_generate_description_different_types(self, client: TestClient):
        """Test description generation for different jewelry types."""
        test_cases = [
            {"jewelry_type": "necklace", "materials": ["Gold"]},
            {"jewelry_type": "bracelet", "materials": ["Silver", "Pearl"]},
            {"jewelry_type": "earrings", "materials": ["Platinum"]}
        ]

        for case in test_cases:
            response = client.post("/api/v1/descriptions/generate", json=case)

            assert response.status_code == 200
            data = response.json()

            assert data["jewelry_type"] == case["jewelry_type"]
            assert data["material_count"] == len(case["materials"])
            assert len(data["description"]) > 0


class TestHealthAndRootEndpointsIntegration:
    """Integration tests for health and root endpoints."""

    def test_health_endpoint(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root API endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "Jewelry Calculator API" in data["message"]
        assert "docs" in data
        assert "health" in data

    def test_calculator_page_template(self, client: TestClient):
        """Test calculator page template rendering."""
        response = client.get("/calculator")

        assert response.status_code == 200

        # Should return HTML content
        content = response.text
        assert "<!DOCTYPE html>" in content
        assert "jewelry" in content.lower()

        # Check for key elements that should be in the template
        assert "Bootstrap" in content or "bootstrap" in content
        assert "static" in content  # Should reference static files


class TestErrorHandlingIntegration:
    """Integration tests for error handling."""

    def test_invalid_material_data(self, client: TestClient):
        """Test error handling for invalid material data."""
        invalid_data = {
            "name": "",  # Empty name should fail validation
            "unit_price": -50.0,  # Negative price should fail
            "unit": "invalid",
            "category": "test"
        }

        response = client.post("/api/v1/materials/", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_invalid_calculator_data(self, client: TestClient):
        """Test error handling for invalid calculator data."""
        invalid_data = {
            "materials": [],  # Empty materials list
            "hours": -5,  # Negative hours
            "hourly_rate": 0,  # Zero rate
            "jewelry_type": "invalid_type"
        }

        response = client.post("/api/v1/calculator/calculate", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_invalid_description_data(self, client: TestClient):
        """Test error handling for invalid description data."""
        invalid_data = {
            "jewelry_type": "crown",  # Invalid jewelry type
            "materials": []  # Empty materials list
        }

        response = client.post("/api/v1/descriptions/generate", json=invalid_data)

        assert response.status_code == 422  # Validation error