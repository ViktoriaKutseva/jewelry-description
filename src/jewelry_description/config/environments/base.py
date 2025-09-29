"""
Base environment settings with common configuration fields.
"""

from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseEnvironmentSettings(BaseSettings):
    """Base settings class with common configuration for all environments."""

    # Application settings
    app_name: str = Field(default="jewelry-description", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    environment: str = Field(default="development", description="Current environment")

    # Debug settings
    debug: bool = Field(default=False, description="Enable debug mode")

    # Database settings
    database_url: str = Field(
        default="sqlite+aiosqlite:///./jewelry.db",
        description="Database connection URL"
    )

    # Web server settings
    web_host: str = Field(default="localhost", description="Web server host")
    web_port: int = Field(default=8000, ge=1, le=65535, description="Web server port")

    # CORS settings
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        description="Log format string"
    )

    # Security settings
    secret_key: str = Field(
        default="changeme-secret-key-for-development-only",
        description="Secret key for JWT tokens and sessions"
    )

    # API settings
    api_prefix: str = Field(default="/api/v1", description="API prefix for endpoints")
    api_title: str = Field(default="Jewelry Description API", description="API title")
    api_description: str = Field(default="API for jewelry cost calculation and description generation", description="API description")
    api_version: str = Field(default="v1", description="API version")

    # Rate limiting
    rate_limit_requests: int = Field(default=100, ge=1, description="Rate limit requests per window")
    rate_limit_window: int = Field(default=60, ge=1, description="Rate limit window in seconds")

    # File upload settings
    max_upload_size: int = Field(default=10 * 1024 * 1024, ge=1024, description="Maximum file upload size in bytes")  # 10MB
    allowed_extensions: List[str] = Field(
        default_factory=lambda: [".csv", ".json"],
        description="Allowed file extensions for upload"
    )

    # Cache settings
    cache_enabled: bool = Field(default=True, description="Enable caching")
    cache_ttl: int = Field(default=300, ge=0, description="Cache TTL in seconds")  # 5 minutes

    # External service settings (placeholders for future use)
    external_api_timeout: int = Field(default=30, ge=1, description="External API timeout in seconds")
    external_api_retries: int = Field(default=3, ge=0, description="External API retry attempts")

    model_config = SettingsConfigDict(
        env_prefix="JEWELRY_",
        env_file=[".env.local", ".env"],
        case_sensitive=False,
        env_nested_delimiter="__"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v.upper()

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v: List[str]) -> List[str]:
        """Validate CORS origins are valid URLs."""
        from urllib.parse import urlparse
        for origin in v:
            parsed = urlparse(origin)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid CORS origin: {origin}")
        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key is not the default insecure value in production."""
        # Allow default value in development/testing environments
        if v == "changeme-secret-key-for-development-only":
            # This will be checked at the environment level
            return v
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v