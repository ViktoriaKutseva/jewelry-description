"""
Dynamic settings configuration based on environment.
"""

import os
from typing import Type

from jewelry_description.config.environments.base import BaseEnvironmentSettings
from jewelry_description.config.environments.development import DevelopmentSettings
from jewelry_description.config.environments.testing import TestingSettings
from jewelry_description.config.environments.staging import StagingSettings
from jewelry_description.config.environments.production import ProductionSettings


def get_settings() -> BaseEnvironmentSettings:
    """
    Get settings for the current environment.

    The environment is determined by the JEWELRY_ENVIRONMENT or ENVIRONMENT
    environment variable, defaulting to 'development'.
    """
    env = os.getenv("JEWELRY_ENVIRONMENT") or os.getenv("ENVIRONMENT", "development")
    env = env.lower()

    settings_map: dict[str, Type[BaseEnvironmentSettings]] = {
        "development": DevelopmentSettings,
        "testing": TestingSettings,
        "staging": StagingSettings,
        "production": ProductionSettings,
    }

    settings_class = settings_map.get(env, DevelopmentSettings)

    try:
        return settings_class()
    except Exception as e:
        # Fallback to development settings if environment-specific settings fail
        print(f"Warning: Failed to load {env} settings: {e}")
        print("Falling back to development settings")
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()
