from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """Database configuration settings."""
    path: str = "data/materials.db"
    timeout: int = 30


class WebSettings(BaseModel):
    """Web server configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


class AppSettings(BaseSettings):
    """Main application settings."""
    app_name: str = "jewelry-description"
    version: str = "0.1.0"
    description: str = "Jewelry price and description creator"
    debug: bool = False
    
    # Database settings
    database: DatabaseSettings = DatabaseSettings()
    
    # Web server settings
    web: WebSettings = WebSettings()
    
    # Log settings
    log_level: str = "INFO"
    log_file: str | None = None
    
    model_config = SettingsConfigDict(
        env_prefix="JEWELRY_",
        env_file=".env",
        env_nested_delimiter="__"
    )


# Global settings instance
settings = AppSettings()
