"""End-to-end tests for the complete web application using API testing."""

from fastapi.testclient import TestClient


class TestJewelryCalculatorWebApplicationE2E:
    """End-to-end tests for the jewelry calculator web application."""

    def test_web_page_loads_successfully(self, client: TestClient):
        """Test that the main calculator web page loads successfully."""
        response = client.get("/calculator")

        assert response.status_code == 200
        content = response.text

        # Check that it's HTML content
        assert "<!DOCTYPE html>" in content
        assert "<html" in content

        # Check for key page elements
        assert "jewelry" in content.lower()
        assert "calculator" in content.lower()

    def test_static_assets_served(self, client: TestClient):
        """Test that static assets are served correctly."""
        # Test CSS file
        response = client.get("/static/css/main.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

        # Test JavaScript file
        response = client.get("/static/js/main.js")
        assert response.status_code == 200
        assert "text/javascript" in response.headers.get("content-type", "")

    def test_api_materials_workflow(self, client: TestClient):
        """Test complete materials API workflow."""
        # 1. Get materials
        response = client.get("/api/v1/materials/")
        assert response.status_code == 200
        materials = response.json()
        assert isinstance(materials, list)
        assert len(materials) > 0

        # 2. Search materials
        response = client.get("/api/v1/materials/search?q=test")
        assert response.status_code == 200
        search_results = response.json()
        assert isinstance(search_results, list)

        # 3. Add custom material
        custom_material = {
            "name": "Custom Platinum",
            "unit_price": 200.0,
            "unit": "г",
            "category": "metal"
        }
        response = client.post("/api/v1/materials/", json=custom_material)
        assert response.status_code == 201
        added_material = response.json()
        assert added_material["name"] == "Custom Platinum"

    def test_api_calculator_workflow(self, client: TestClient):
        """Test complete calculator API workflow."""
        # Calculate cost with materials
        calculation_request = {
            "materials": [
                {
                    "name": "Silver",
                    "unit_price": 25.0,
                    "quantity": 10.0,
                    "unit": "г"
                },
                {
                    "name": "Diamond",
                    "unit_price": 500.0,
                    "quantity": 1.0,
                    "unit": "шт"
                }
            ],
            "hours": 2.5,
            "hourly_rate": 150.0,
            "jewelry_type": "ring",
            "consumables": [
                {
                    "name": "Polishing compound",
                    "approx_cost": 75.0
                }
            ],
            "extra_costs": [
                {
                    "name": "Packaging",
                    "approx_cost": 50.0
                }
            ],
            "electricity_cost": 25.0,
            "tool_depreciation": 15.0,
            "defect_percent": 5.0
        }

        response = client.post("/api/v1/calculator/calculate", json=calculation_request)
        assert response.status_code == 200

        result = response.json()

        # Verify complete response structure
        required_fields = [
            "total_cost", "cost_breakdown", "recommended_prices",
            "price_comment", "calculation_metadata"
        ]
        for field in required_fields:
            assert field in result

        # Verify cost is reasonable
        assert result["total_cost"] > 0

        # Verify recommended prices (2x, 2.5x, 3x)
        prices = result["recommended_prices"]
        assert prices["minimum"] >= result["total_cost"] * 2
        assert prices["comfort"] >= result["total_cost"] * 2.5
        assert prices["premium"] >= result["total_cost"] * 3

        # Verify metadata
        metadata = result["calculation_metadata"]
        assert metadata["material_count"] == 2
        assert metadata["has_consumables"] is True
        assert metadata["has_extra_costs"] is True
        assert metadata["defect_percentage"] == 5.0

    def test_api_descriptions_workflow(self, client: TestClient):
        """Test complete descriptions API workflow."""
        # Generate description
        description_request = {
            "jewelry_type": "necklace",
            "materials": ["Gold", "Pearl", "Diamond"]
        }

        response = client.post("/api/v1/descriptions/generate", json=description_request)
        assert response.status_code == 200

        result = response.json()

        # Verify response structure
        assert "description" in result
        assert "jewelry_type" in result
        assert "material_count" in result
        assert "hashtags" in result

        # Verify content
        assert result["jewelry_type"] == "necklace"
        assert result["material_count"] == 3
        assert len(result["description"]) > 0
        assert isinstance(result["hashtags"], list)
        assert len(result["hashtags"]) > 0

        # Check that jewelry type is in hashtags
        assert any("#necklace" in tag for tag in result["hashtags"])

    def test_health_and_root_endpoints(self, client: TestClient):
        """Test health check and root endpoints."""
        # Health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        assert "version" in health_data
        assert "timestamp" in health_data

        # Root endpoint
        response = client.get("/")
        assert response.status_code == 200
        root_data = response.json()
        assert "message" in root_data
        assert "docs" in root_data

    def test_error_handling_validation(self, client: TestClient):
        """Test error handling for invalid requests."""
        # Invalid calculator request
        invalid_request = {
            "materials": [],
            "hours": -1,
            "hourly_rate": 0,
            "jewelry_type": "invalid_type"
        }

        response = client.post("/api/v1/calculator/calculate", json=invalid_request)
        assert response.status_code == 422  # Validation error

        # Invalid description request
        invalid_description = {
            "jewelry_type": "crown",  # Not supported
            "materials": []
        }

        response = client.post("/api/v1/descriptions/generate", json=invalid_description)
        assert response.status_code == 422  # Validation error

    def test_complete_user_workflow_simulation(self, client: TestClient):
        """Simulate a complete user workflow through the API."""
        # Step 1: Get available materials
        response = client.get("/api/v1/materials/?limit=5")
        assert response.status_code == 200
        materials = response.json()
        assert len(materials) <= 5

        # Step 2: Calculate cost for a ring
        calc_request = {
            "materials": [
                {
                    "name": "Silver",
                    "unit_price": 25.0,
                    "quantity": 8.0,
                    "unit": "г"
                }
            ],
            "hours": 2.0,
            "hourly_rate": 120.0,
            "jewelry_type": "ring"
        }

        response = client.post("/api/v1/calculator/calculate", json=calc_request)
        assert response.status_code == 200
        calc_result = response.json()

        # Step 3: Generate description for the same ring
        desc_request = {
            "jewelry_type": "ring",
            "materials": ["Silver"]
        }

        response = client.post("/api/v1/descriptions/generate", json=desc_request)
        assert response.status_code == 200
        desc_result = response.json()

        # Step 4: Verify both results are consistent
        assert calc_result["calculation_metadata"]["material_count"] == 1
        assert desc_result["material_count"] == 1
        assert desc_result["jewelry_type"] == "ring"

        # Step 5: Verify total workflow completed successfully
        assert calc_result["total_cost"] > 0
        assert len(desc_result["description"]) > 0

    def test_api_rate_limiting_and_performance(self, client: TestClient):
        """Test API performance and basic rate limiting."""
        import time

        # Test multiple calculator requests
        calc_request = {
            "materials": [{"name": "Copper", "unit_price": 15.0, "quantity": 10.0, "unit": "г"}],
            "hours": 1.0,
            "hourly_rate": 100.0,
            "jewelry_type": "bracelet"
        }

        start_time = time.time()
        for _ in range(5):
            response = client.post("/api/v1/calculator/calculate", json=calc_request)
            assert response.status_code == 200
        end_time = time.time()

        # Should complete within reasonable time (less than 2 seconds for 5 requests)
        assert end_time - start_time < 2.0

    def test_template_rendering_and_static_files(self, client: TestClient):
        """Test that templates render correctly and reference static files."""
        response = client.get("/calculator")
        assert response.status_code == 200

        content = response.text

        # Check for template content
        assert "<html" in content
        assert "</html>" in content

        # Check for static file references
        assert "/static/css/main.css" in content
        assert "/static/js/main.js" in content

        # Check that static files are actually accessible
        css_response = client.get("/static/css/main.css")
        assert css_response.status_code == 200

        js_response = client.get("/static/js/main.js")
        assert js_response.status_code == 200