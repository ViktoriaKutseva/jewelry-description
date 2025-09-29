"""
Development environment settings.
"""

from jewelry_description.config.environments.base import BaseEnvironmentSettings


class DevelopmentSettings(BaseEnvironmentSettings):
    """Settings for development environment."""

    # Environment identification
    environment: str = "development"

    # Debug settings
    debug: bool = True

    # Database settings - local SQLite for development
    database_url: str = "sqlite+aiosqlite:///./dev_jewelry.db"

    # Web server settings
    web_host: str = "localhost"
    web_port: int = 8000

    # CORS settings - allow local development origins
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Logging settings
    log_level: str = "DEBUG"

    # Development-specific settings
    auto_reload: bool = True  # Enable auto-reload for development
    show_error_details: bool = True  # Show detailed error information

    # Relaxed rate limiting for development
    rate_limit_requests: int = 1000
    rate_limit_window: int = 60

    # Development cache settings
    cache_enabled: bool = False  # Disable caching in development for easier debugging