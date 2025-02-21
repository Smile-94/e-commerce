from enum import Enum
from typing import Any

from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.env import env_config


class DatabaseChoices(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SQLITE = "sqlite3"


class DatabaseSettings(BaseSettings):
    """
    This class defines the setting configuration for this auth service
    """

    # General Database Configuration
    DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

    # Redis Configuration
    REDIS_HOST: SecretStr = Field(default="localhost", frozen=True, repr=False)
    REDIS_PORT: int = Field(default=6379, frozen=True, repr=False)

    # Data base choices
    DATABASE_CHOICES: str = Field(
        default=DatabaseChoices.SQLITE, frozen=True, repr=False
    )

    # Database Configuration
    DATABASE_HOST: SecretStr = Field(default="localhost", frozen=True, repr=False)
    DATABASE_PORT: int = Field(default=5432, frozen=True, repr=False)
    DATABASE_NAME: SecretStr = Field(default="postgres", frozen=True, repr=False)
    DATABASE_USER: SecretStr = Field(default="postgres", frozen=True, repr=False)
    DATABASE_PASSWORD: SecretStr = Field(default="postgres", frozen=True, repr=False)

    ATOMIC_DB: bool = Field(default=True, frozen=True, repr=False)

    model_config = SettingsConfigDict(
        env_file=env_config.env_file,
        extra="ignore",
        case_sensitive=True,
    )

    @computed_field()
    def DATABASES(self) -> dict[str, Any]:
        if self.DATABASE_CHOICES == "sqlite3":
            return {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": "db.sqlite3",
                }
            }
        elif self.DATABASE_CHOICES == "mysql":
            return {
                "default": {
                    "ENGINE": "django.db.backends.mysql",
                    "NAME": self.DATABASE_NAME.get_secret_value(),  # Database name
                    "USER": self.DATABASE_NAME.get_secret_value(),  # MySQL username
                    "PASSWORD": self.DATABASE_PASSWORD.get_secret_value(),  # MySQL password
                    "HOST": self.DATABASE_HOST.get_secret_value(),  # Database host (use 'localhost' for local development)
                    "PORT": self.DATABASE_PORT,  # Database port (default is 3306)
                }
            }

        elif self.DATABASE_CHOICES == "postgres":
            return {
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": self.DATABASE_NAME.get_secret_value(),
                    "USER": self.DATABASE_NAME.get_secret_value(),
                    "PASSWORD": self.DATABASE_PASSWORD.get_secret_value(),
                    "HOST": self.DATABASE_HOST.get_secret_value(),
                    "PORT": self.DATABASE_PORT,
                },
            }


db_config = DatabaseSettings()
