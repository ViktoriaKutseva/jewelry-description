"""
Production environment settings.
"""

from pydantic import Field, SecretStr, field_validator
from jewelry_description.config.environments.base import BaseEnvironmentSettings


class ProductionSettings(BaseEnvironmentSettings):
    """Settings for production environment."""

    # Environment identification
    environment: str = "production"

    # Debug settings - never debug in production
    debug: bool = False

    # Database settings - production database (required)
    database_url: SecretStr = Field(
        ...,
        description="Production database URL (required)"
    )

    # Web server settings
    web_host: str = "0.0.0.0"
    web_port: int = 8000

    # CORS settings - production domains only
    cors_origins: list[str] = Field(
        default_factory=list,
        description="Production CORS origins (configured via environment)"
    )

    # Logging settings - structured logging for production
    log_level: str = "WARNING"

    # Security settings - strong secret required
    secret_key: SecretStr = Field(
        ...,
        description="Production secret key (required)",
        min_length=64
    )

    # Rate limiting - strict for production
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    # Production cache settings
    cache_enabled: bool = True
    cache_ttl: int = 1800  # 30 minutes

    # Production timeouts
    external_api_timeout: int = 30
    external_api_retries: int = 3

    # Production monitoring
    monitoring_enabled: bool = True
    metrics_enabled: bool = True
    health_checks_enabled: bool = True

    # Security headers
    security_headers_enabled: bool = True
    hsts_enabled: bool = True
    csp_enabled: bool = True

    # Performance settings
    connection_pool_size: int = Field(default=10, ge=1, le=100)
    max_connections: int = Field(default=100, ge=1, le=1000)

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v: list[str]) -> list[str]:
        """Validate production CORS origins are HTTPS only."""
        if not v:
            return v

        for origin in v:
            if not origin.startswith("https://"):
                raise ValueError(f"Production CORS origins must use HTTPS: {origin}")
        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: SecretStr) -> SecretStr:
        """Validate production secret key is strong."""
        secret_value = v.get_secret_value()
        if len(secret_value) < 64:
            raise ValueError("Production secret key must be at least 64 characters long")
        if secret_value == "staging-secret-key-change-in-production":
            raise ValueError("Production secret key must be changed from staging default")
        if secret_value == "changeme-secret-key-for-development-only":
            raise ValueError("Production secret key must be changed from development default")
        return v