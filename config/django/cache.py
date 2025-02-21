from enum import Enum
from typing import Any

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.django.database import db_config
from config.env import env_config


class CacheBackendChoice(Enum):
    REDIS = "redis"
    MEMCACHE = "memcached"


class CacheSettings(BaseSettings):
    """
    This class defines the setting configuration for this auth service
    """

    CACHE_TTL: int = 60 * 1500
    REDIS_CACHE_BACKEND: str = Field(
        default="django.core.cache.backends.redis.RedisCache",
        frozen=True,
        repr=False,
    )

    CACHE_BACKEND_CHOICES: str = Field(
        default=CacheBackendChoice.MEMCACHE,
        frozen=True,
        repr=False,
    )

    model_config = SettingsConfigDict(
        env_file=env_config.env_file,
        extra="ignore",
        case_sensitive=True,
    )

    @computed_field()
    def CACHES(self) -> dict[str, Any]:
        if self.CACHE_BACKEND_CHOICES == "redis":
            # This computed field returns the CACHES configuration based on the provided settings.
            # This line will connect to the Redis cache server.
            # Make sure to replace 'yourpassword' with the actual password for your Redis server.
            return {
                "default": {
                    "BACKEND": self.REDIS_CACHE_BACKEND,
                    "LOCATION": f"redis://{db_config.REDIS_HOST.get_secret_value()}:{db_config.REDIS_PORT}",
                    "OPTIONS": {
                        # 'PASSWORD': 'yourpassword',  # Make sure this line is commented out or removed
                    },
                },
            }

        if self.CACHE_BACKEND_CHOICES == "memcached":
            return {
                "default": {
                    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                    "LOCATION": "127.0.0.1:11211",
                }
            }


cache_config = CacheSettings()
