from enum import Enum
from typing import Any

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.django.database import db_config
from config.env import env_config


class ChannelLayerChoices(Enum):
    """
    Enum to define possible channel layer backends.
    """

    REDIS = "redis"
    IN_MEMORY = "in_memory"


class ChannelSettings(BaseSettings):
    """
    This class defines the setting configuration for the channel layer.
    """

    CHANNEL_LAYER_BACKEND: str = Field(
        default=ChannelLayerChoices.IN_MEMORY,
        frozen=True,
    )

    model_config = SettingsConfigDict(
        env_file=env_config.env_file,
        extra="ignore",
        case_sensitive=True,
    )

    @computed_field()
    def CHANNEL_LAYERS(self) -> dict[str, Any]:
        if self.CHANNEL_LAYER_BACKEND == "redis":
            # This computed field returns the CHANNEL_LAYERS configuration based on the provided settings.
            # This line will connect to the Redis channel layer server.
            # Make sure to replace 'yourpassword' with the actual password for your Redis server.
            return {
                "default": {
                    "BACKEND": "channels_redis.core.RedisChannelLayer",
                    "CONFIG": {
                        "hosts": [
                            (
                                db_config.REDIS_HOST.get_secret_value(),
                                db_config.REDIS_PORT,
                            ),
                        ],
                    },
                },
            }

        if self.CHANNEL_LAYER_BACKEND == "in_memory":
            return {
                "default": {
                    "BACKEND": "channels.layers.InMemoryChannelLayer",
                },
            }


channel_config = ChannelSettings()
