from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    materials_file: str = "materials.json"

settings = Settings()