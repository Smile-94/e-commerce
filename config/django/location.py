from pydantic_settings import BaseSettings


class LocationSettings(BaseSettings):
    """
    This class defines the setting configuration for this auth service
    """

    # Internationalization
    INTERNAL_IPS: tuple[str, ...] = ("127.0.0.1",)
    LANGUAGE_CODE: str = "en-us"
    TIME_ZONE: str = "UTC"
    USE_I18N: bool = True
    USE_TZ: bool = True


location_config = LocationSettings()
