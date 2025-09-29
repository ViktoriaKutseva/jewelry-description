"""Unit tests for web API routes with mocked dependencies."""

from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from jewelry_description.models.entities import Material


class TestMaterialsRoutes:
    """Test materials API endpoints."""

    def test_get_materials_success(self, client: TestClient):
        """Test successful retrieval of materials."""
        # Mock the repository
        mock_repo = Mock()
        mock_materials = [
            Material(name="Silver", unit_price=25.0, quantity=0, unit="г"),
            Material(name="Gold", unit_price=150.0, quantity=0, unit="г"),
        ]
        mock_repo.get_filtered_materials.return_value = mock_materials

        with patch("jewelry_description.entrypoints.web.routes.materials.get_material_repository") as mock_get_repo:
            mock_get_repo.return_value = mock_repo

            response = client.get("/api/v1/materials/")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Silver"
            assert data[0]["unit_price"] == 25.0
            assert data[0]["unit"] == "г"

    def test_get_materials_with_search(self, client: TestClient):
        """Test materials retrieval with search filter."""
        mock_repo = Mock()
        mock_materials = [
            Material(name="Silver Ring", unit_price=25.0, quantity=0, unit="г"),
            Material(name="Gold Chain", unit_price=150.0, quantity=0, unit="г"),
        ]
        mock_repo.load_materials_from_csv.return_value = mock_materials

        with patch("jewelry_description.entrypoints.web.routes.materials.get_material_repository") as mock_get_repo:
            mock_get_repo.return_value = mock_repo

            response = client.get("/api/v1/materials/?search=silver")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["name"] == "Silver Ring"

    def test_add_material_success(self, client: TestClient, sample_material_data: dict):
        """Test successful addition of custom material."""
        response = client.post("/api/v1/materials/", json=sample_material_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_material_data["name"]
        assert data["unit_price"] == sample_material_data["unit_price"]
        assert data["unit"] == sample_material_data["unit"]

    def test_add_material_invalid_data(self, client: TestClient):
        """Test addition of material with invalid data."""
        invalid_data = {
            "name": "",  # Invalid: empty name
            "unit_price": -10.0,  # Invalid: negative price
            "unit": "invalid_unit"
        }

        response = client.post("/api/v1/materials/", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_search_materials_success(self, client: TestClient):
        """Test successful material search."""
        mock_repo = Mock()
        mock_materials = [
            Material(name="Silver", unit_price=25.0, quantity=0, unit="г"),
            Material(name="Silver Wire", unit_price=30.0, quantity=0, unit="г"),
        ]
        mock_repo.load_materials_from_csv.return_value = mock_materials

        with patch("jewelry_description.entrypoints.web.routes.materials.get_material_repository") as mock_get_repo:
            mock_get_repo.return_value = mock_repo

            response = client.get("/api/v1/materials/search?q=silver")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert all("silver" in item["name"].lower() for item in data)


class TestCalculatorRoutes:
    """Test calculator API endpoints."""

    def test_calculate_cost_success(self, client: TestClient, sample_calculator_data: dict):
        """Test successful cost calculation."""
        # Mock the calculator service
        mock_calculator = Mock()
        mock_result = Mock()
        mock_result.total_cost = 575.0
        mock_result.cost_breakdown = {
            "Silver (10.0 г)": 250.0,
            "Время (2.0 ч)": 300.0,
            "Расходники": 25.0
        }
        mock_result.recommended_prices = {
            "Минимальная (×2)": 1150.0,
            "Комфортная (×2.5)": 1437.5,
            "Премиум (×3)": 1725.0
        }
        mock_result.price_comment = "Рекомендуемая цена: 1437.50 руб."
        mock_calculator.calculate_cost.return_value = mock_result

        with patch("jewelry_description.entrypoints.web.routes.calculator.get_cost_calculator") as mock_get_calc:
            mock_get_calc.return_value = mock_calculator

            response = client.post("/api/v1/calculator/calculate", json=sample_calculator_data)

            assert response.status_code == 200
            data = response.json()
            assert data["total_cost"] == 575.0
            assert "recommended_prices" in data
            assert "cost_breakdown" in data
            assert "calculation_metadata" in data

    def test_calculate_cost_invalid_data(self, client: TestClient):
        """Test cost calculation with invalid data."""
        invalid_data = {
            "materials": [],
            "hours": -1,  # Invalid: negative hours
            "hourly_rate": 0,  # Invalid: zero rate
            "jewelry_type": ""
        }

        response = client.post("/api/v1/calculator/calculate", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_calculate_cost_service_error(self, client: TestClient, sample_calculator_data: dict):
        """Test cost calculation when service raises an error."""
        mock_calculator = Mock()
        mock_calculator.calculate_cost.side_effect = Exception("Calculation failed")

        with patch("jewelry_description.entrypoints.web.routes.calculator.get_cost_calculator") as mock_get_calc:
            mock_get_calc.return_value = mock_calculator

            response = client.post("/api/v1/calculator/calculate", json=sample_calculator_data)

            assert response.status_code == 500
            data = response.json()
            assert "Failed to calculate jewelry cost" in data["detail"]


class TestDescriptionsRoutes:
    """Test descriptions API endpoints."""

    def test_generate_description_success(self, client: TestClient, sample_description_data: dict):
        """Test successful description generation."""
        # Mock the description generator
        mock_generator = Mock()
        mock_description = "A mystical silver ring that captures the essence of the moon's gentle glow."
        mock_generator.generate_description.return_value = mock_description

        with patch("jewelry_description.entrypoints.web.routes.descriptions.get_description_generator") as mock_get_gen:
            mock_get_gen.return_value = mock_generator

            response = client.post("/api/v1/descriptions/generate", json=sample_description_data)

            assert response.status_code == 200
            data = response.json()
            assert data["description"] == mock_description
            assert data["jewelry_type"] == sample_description_data["jewelry_type"]
            assert data["material_count"] == len(sample_description_data["materials"])
            assert "hashtags" in data

    def test_generate_description_invalid_jewelry_type(self, client: TestClient):
        """Test description generation with invalid jewelry type."""
        invalid_data = {
            "jewelry_type": "invalid_type",
            "materials": ["Silver"]
        }

        response = client.post("/api/v1/descriptions/generate", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_generate_description_service_error(self, client: TestClient, sample_description_data: dict):
        """Test description generation when service raises an error."""
        mock_generator = Mock()
        mock_generator.generate_description.side_effect = Exception("Generation failed")

        with patch("jewelry_description.entrypoints.web.routes.descriptions.get_description_generator") as mock_get_gen:
            mock_get_gen.return_value = mock_generator

            response = client.post("/api/v1/descriptions/generate", json=sample_description_data)

            assert response.status_code == 500
            data = response.json()
            assert "Failed to generate jewelry description" in data["detail"]


class TestHealthRoutes:
    """Test health check endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "health" in data

    def test_calculator_page(self, client: TestClient):
        """Test calculator page endpoint."""
        response = client.get("/calculator")

        assert response.status_code == 200
        # Should return HTML content
        assert "text/html" in response.headers.get("content-type", "")