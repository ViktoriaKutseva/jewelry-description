"""
Staging environment settings.
"""

from pydantic import Field, SecretStr
from jewelry_description.config.environments.base import BaseEnvironmentSettings


class StagingSettings(BaseEnvironmentSettings):
    """Settings for staging environment."""

    # Environment identification
    environment: str = "staging"

    # Debug settings - limited debug for staging
    debug: bool = False

    # Database settings - staging database
    database_url: SecretStr = Field(
        default=SecretStr("sqlite+aiosqlite:///./staging_jewelry.db"),
        description="Staging database URL"
    )

    # Web server settings
    web_host: str = "0.0.0.0"
    web_port: int = 8000

    # CORS settings - staging domain
    cors_origins: list[str] = [
        "https://staging.jewelry-description.com",
        "https://staging-api.jewelry-description.com",
    ]

    # Logging settings
    log_level: str = "INFO"

    # Security settings - staging secret
    secret_key: str = Field(
        default="staging-secret-key-change-in-production",
        min_length=32
    )

    # Rate limiting - moderate for staging
    rate_limit_requests: int = 500
    rate_limit_window: int = 60

    # Enable caching in staging
    cache_enabled: bool = True
    cache_ttl: int = 600  # 10 minutes

    # Staging-specific settings
    monitoring_enabled: bool = True
    health_checks_enabled: bool = True