"""
Testing environment settings.
"""

from jewelry_description.config.environments.base import BaseEnvironmentSettings


class TestingSettings(BaseEnvironmentSettings):
    """Settings for testing environment."""

    # Environment identification
    environment: str = "testing"

    # Debug settings
    debug: bool = True

    # Database settings - in-memory SQLite for fast testing
    database_url: str = "sqlite+aiosqlite:///:memory:"

    # Web server settings - use different port to avoid conflicts
    web_host: str = "localhost"
    web_port: int = 8001

    # CORS settings - minimal for testing
    cors_origins: list[str] = [
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ]

    # Logging settings - quiet logging for tests
    log_level: str = "WARNING"

    # Test-specific settings
    skip_auth: bool = True  # Skip authentication in tests
    skip_rate_limiting: bool = True  # Skip rate limiting in tests

    # Very relaxed rate limiting for tests
    rate_limit_requests: int = 10000
    rate_limit_window: int = 1

    # Disable caching in tests
    cache_enabled: bool = False

    # Fast timeouts for tests
    external_api_timeout: int = 5
    external_api_retries: int = 0

    # Test data settings
    test_data_enabled: bool = True
    mock_external_services: bool = True