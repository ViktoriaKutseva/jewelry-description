from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "jewelry-description"
    version: str = "0.1.0"
    debug: bool = False

    # Database settings (for future use)
    database_url: str = "sqlite+aiosqlite:///./jewelry.db"

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="JEWELRY_",
        env_file=[".env.local", ".env"],
        case_sensitive=False,
    )


settings = Settings()
