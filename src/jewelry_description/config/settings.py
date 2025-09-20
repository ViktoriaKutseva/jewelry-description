from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppSettings(BaseSettings):
    app_name: str = "jewelry-description"
    debug: bool = True
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")

settings = AppSettings()
