from typing import Any

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class SchemaSettings(BaseSettings):
    """
    Settings for drf-spectacular
    """

    SCHEMA_PATH_PREFIX: str = Field(default="/api/v1")
    SCHEMA_PATH_PREFIX_TRIM: bool = Field(default=True)
    TITLE: str = Field(default="Project API")
    DESCRIPTION: str = Field(
        default="Details about your project",
    )
    VERSION: str = Field(default="1.0.0")
    CONTACT: dict[str, Any] = Field(
        default={
            "name": "Md. Sazzad Hossen",
            "url": "https://github.com/smile-94/",
            "email": "mshossen75@gmail.com",
        },
    )
    LICENSE: dict[str, Any] = Field(
        default={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    )
    TERMS_OF_SERVICE: str = Field(
        default="",
    )
    SERVERS: list = Field(
        default=[
            {"url": "http://localhost:8000", "description": "Default Local Server"},
            {
                "url": "http://192.168.10.246:8001",
                "description": "Local Development Server",
            },
        ],
    )

    @computed_field()
    def SPECTACULAR_SETTINGS(self) -> dict[str, Any]:
        return {
            "TITLE": self.TITLE,
            "DESCRIPTION": self.DESCRIPTION,
            "VERSION": self.VERSION,
            "CONTACT": self.CONTACT,
            "LICENSE": self.LICENSE,
            "TERMS_OF_SERVICE": self.TERMS_OF_SERVICE,
            "SCHEMA_PATH_PREFIX": self.SCHEMA_PATH_PREFIX,
            "SCHEMA_PATH_PREFIX_TRIM": self.SCHEMA_PATH_PREFIX_TRIM,
            "SERVERS": self.SERVERS,
        }


# Load the schema configuration
schema_config = SchemaSettings()
