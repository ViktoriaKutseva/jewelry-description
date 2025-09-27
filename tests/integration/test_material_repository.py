"""Integration tests for CSV material repository."""

from jewelry_description.integrations.database.repositories import CsvMaterialRepository
from jewelry_description.models.entities import Material


class TestCsvMaterialRepository:
    """Test CSV material repository integration."""

    def test_load_materials_from_csv(self):
        """Test loading materials from CSV file."""
        repo = CsvMaterialRepository()
        materials = repo.load_materials_from_csv("info.csv")

        assert len(materials) > 0
        assert all(isinstance(mat, Material) for mat in materials)

        # Check that materials have valid data
        for material in materials[:5]:  # Test first 5
            assert material.name
            assert material.unit_price > 0
            assert material.unit in ["г", "шт"]
            assert material.quantity == 0  # Repository sets quantity to 0

    def test_find_material_by_name(self):
        """Test finding material by name."""
        repo = CsvMaterialRepository()

        # Test exact match
        copper = repo.find_material_by_name("Copper")
        assert copper is not None
        assert "copper" in copper.name.lower()
        assert copper.unit_price > 0

        # Test partial match
        brass = repo.find_material_by_name("Brass")
        assert brass is not None
        assert "brass" in brass.name.lower()

        # Test case insensitive
        wire = repo.find_material_by_name("wire")
        assert wire is not None

        # Test non-existent material
        nonexistent = repo.find_material_by_name("nonexistent_material_12345")
        assert nonexistent is None

    def test_get_filtered_materials(self):
        """Test getting filtered materials."""
        repo = CsvMaterialRepository()
        filtered = repo.get_filtered_materials("info.csv")

        assert len(filtered) > 0
        assert all(isinstance(mat, Material) for mat in filtered)

        # Check that filtered materials have proper names and prices
        material_names = [mat.name for mat in filtered]
        assert (
            "Квадратная медь (средняя)" in material_names
        )  # Square copper is separate
        assert "Латунь (средняя)" in material_names
        assert "Нейзильбер (средняя)" in material_names

        # Check that all filtered materials have valid prices
        for material in filtered:
            assert material.unit_price > 0
            assert material.unit in ["г", "шт"]  # Can be per gram or per piece

    def test_repository_interface_compliance(self):
        """Test that repository implements the MaterialRepository interface."""
        repo = CsvMaterialRepository()

        # Test that all interface methods exist
        assert hasattr(repo, "load_materials_from_csv")
        assert hasattr(repo, "find_material_by_name")
        assert hasattr(repo, "get_filtered_materials")

        # Test method signatures by calling them
        materials = repo.load_materials_from_csv("info.csv")
        assert isinstance(materials, list)

        found = repo.find_material_by_name("test")
        assert found is None or isinstance(found, Material)

        filtered = repo.get_filtered_materials("info.csv")
        assert isinstance(filtered, list)
