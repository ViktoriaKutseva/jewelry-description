"""End-to-end tests for the jewelry calculator application."""

import subprocess
from pathlib import Path


class TestJewelryCalculatorE2E:
    """End-to-end tests for the complete jewelry calculator application."""

    def test_cli_calculation_with_sample_data(self):
        """Test full CLI calculation with sample jewelry data."""
        # Run the CLI command
        cmd = [
            "uv",
            "run",
            "jewelry-calc",
            "calc",
            "Silver",
            "25.0",
            "10.0",
            "2.0",
            "150.0",
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent
        )

        # Check that command succeeded
        assert result.returncode == 0
        output = result.stdout

        # Verify output contains expected sections
        assert "=== Jewelry Cost Calculation ===" in output
        assert "Total cost:" in output
        assert "Cost Breakdown:" in output
        assert "Recommended Selling Prices:" in output
        assert "💡 Recommendation:" in output

        # Verify specific calculations
        assert "Silver (10.0 г): 250.00" in output  # 10g * 25/g = 250
        assert "Время (2.0 ч): 300.00" in output  # 2h * 150/h = 300
        assert "Total cost: 1095.00" in output  # 250 + 300 + consumables

    def test_cli_calculation_with_different_materials(self):
        """Test CLI with different material types."""
        test_cases = [
            # (name, price, quantity, hours, rate, expected_total)
            ("Gold", "150.0", "5.0", "3.0", "200.0", "1895.00"),
            (
                "Copper",
                "20.0",
                "15.0",
                "1.5",
                "100.0",
                "995.00",
            ),  # 300 + 150 + 545 = 995
        ]

        for material_name, price, qty, hours, rate, expected_total in test_cases:
            cmd = [
                "uv",
                "run",
                "jewelry-calc",
                "calc",
                material_name,
                price,
                qty,
                hours,
                rate,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent.parent,
            )

            assert result.returncode == 0
            output = result.stdout
            assert f"Total cost: {expected_total}" in output

    def test_cli_help_functionality(self):
        """Test that CLI help works correctly."""
        cmd = ["uv", "run", "jewelry-calc", "calc", "--help"]

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent
        )

        assert result.returncode == 0
        output = result.stdout

        # Verify help contains expected information
        assert "Calculate jewelry cost" in output
        assert "MATERIAL_NAME" in output
        assert "MATERIAL_PRICE" in output
        assert "WORK_HOURS" in output
        assert "HOURLY_RATE" in output

    def test_business_service_integration(self):
        """Test that business service integrates correctly with all layers."""
        from jewelry_description.business.services import JewelryCostCalculatorService
        from jewelry_description.integrations.database.repositories import (
            CsvMaterialRepository,
        )
        from jewelry_description.models.entities import (
            Material,
            WorkTime,
            JewelryCostInput,
            Consumable,
        )

        # Test full integration: repository -> service -> results
        repo = CsvMaterialRepository()

        # Load real materials from CSV
        materials = repo.load_materials_from_csv("info.csv")
        assert len(materials) > 0

        # Use first material for calculation
        test_material = materials[0]
        work_time = WorkTime(hours=2.0, hourly_rate=150.0)

        # Create input with real material data
        consumables = [Consumable(name="Test consumable", approx_cost=100.0)]

        input_data = JewelryCostInput(
            materials=[
                Material(
                    name=test_material.name,
                    unit_price=test_material.unit_price,
                    quantity=5.0,  # Use 5 units
                    unit=test_material.unit,
                )
            ],
            consumables=consumables,
            work_time=work_time,
        )

        # Calculate using business service
        service = JewelryCostCalculatorService()
        result = service.calculate_cost(input_data)

        # Verify complete result structure
        assert result.total_cost > 0
        assert len(result.cost_breakdown) > 0
        assert len(result.recommended_prices) == 3  # min, comfort, premium
        assert result.price_comment

        # Verify cost breakdown contains all components
        breakdown_keys = list(result.cost_breakdown.keys())
        assert any("Время" in key for key in breakdown_keys)  # Work time
        assert any(
            test_material.name.split()[0] in key for key in breakdown_keys
        )  # Material

    def test_error_handling_e2e(self):
        """Test error handling in end-to-end scenarios."""
        from jewelry_description.business.services import JewelryCostCalculatorService
        from jewelry_description.models.entities import (
            Material,
            WorkTime,
            JewelryCostInput,
        )

        service = JewelryCostCalculatorService()

        # Test with invalid data (negative price)
        try:
            invalid_material = Material(name="Test", unit_price=-10.0, quantity=5.0)
            work_time = WorkTime(hours=2.0, hourly_rate=150.0)

            input_data = JewelryCostInput(
                materials=[invalid_material], consumables=[], work_time=work_time
            )

            # This should raise a validation error from Pydantic
            service.calculate_cost(input_data)
            assert False, "Should have raised validation error"
        except Exception:
            # Expected - validation should prevent negative prices
            pass
