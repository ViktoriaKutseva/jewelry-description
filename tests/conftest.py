"""Test configuration and fixtures for jewelry description tests."""

import asyncio
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from jewelry_description.config.settings import Settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings."""
    settings = Settings()
    settings.debug = True
    settings.web_host = "localhost"
    settings.web_port = 8000
    return settings


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create FastAPI test client."""
    from jewelry_description.entrypoints.web.main import app
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_material_data() -> dict:
    """Sample material data for testing."""
    return {
        "name": "Test Silver",
        "unit_price": 25.0,
        "unit": "г",
        "category": "metal"
    }


@pytest.fixture
def sample_calculator_data() -> dict:
    """Sample calculator input data for testing."""
    return {
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
        "jewelry_type": "ring"
    }


@pytest.fixture
def sample_description_data() -> dict:
    """Sample description generation data for testing."""
    return {
        "materials": ["Silver", "Diamond"],
        "jewelry_type": "ring",
        "style": "elegant"
    }


@pytest.fixture
def mock_csv_file(tmp_path: Path) -> Path:
    """Create a mock CSV file for testing."""
    csv_content = """Name,1 gram,1 piece
Test Silver,25.0,
Test Gold,150.0,
Test Diamond,,500.0
Test Copper,15.0,
"""
    csv_file = tmp_path / "test_materials.csv"
    csv_file.write_text(csv_content)
    return csv_file


@pytest.fixture
def test_data_dir(tmp_path: Path, mock_csv_file: Path) -> Path:
    """Create test data directory with sample files."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()

    # Copy mock CSV file
    test_csv = data_dir / "materials.csv"
    test_csv.write_text(mock_csv_file.read_text())

    return data_dir