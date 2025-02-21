import os
from pathlib import PosixPath
from typing import Any

from pydantic_settings import BaseSettings

from config.django.general import general_config


class StaticSettings(BaseSettings):
    """
    This class defines the setting configuration for this auth service
    """

    STATIC_URL: str = "/static/"
    STATIC_ROOT: PosixPath = os.path.join(general_config.BASE_DIR, "static")
    # STATICFILES_STORAGE: str = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    STORAGES: dict[str, dict[str, Any]] = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    MEDIA_URL: str = "/media/"
    MEDIA_ROOT: PosixPath = os.path.join(general_config.BASE_DIR, "media")


static_config = StaticSettings()
