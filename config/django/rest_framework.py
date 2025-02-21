from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class DRFSettings(BaseSettings):
    """
    Settings for Django Rest Framework
    """

    REST_FRAMEWORK: dict[str, Any] = Field(
        default={
            "EXCEPTION_HANDLER": "apps.api.exception_handlers.drf_default_with_modifications_exception_handler",
            # Alternative exception handler
            # 'EXCEPTION_HANDLER': 'styleguide_example.api.exception_handlers.hacksoft_proposed_exception_handler',
            "DEFAULT_FILTER_BACKENDS": (
                "django_filters.rest_framework.DjangoFilterBackend",
            ),
            # "DEFAULT_AUTHENTICATION_CLASSES": [
            #     "apps.authentication.backend.Authentication",
            # ],
            "DEFAULT_PERMISSION_CLASSES": [
                "rest_framework.permissions.AllowAny",
            ],
            "DEFAULT_PARSER_CLASSES": (
                "rest_framework.parsers.JSONParser",
                "rest_framework.parsers.FormParser",
                "rest_framework.parsers.MultiPartParser",
            ),
            "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        },
        frozen=True,
    )


# Instantiate settings
drf_config = DRFSettings()
