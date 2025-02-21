from pydantic import Field
from pydantic_settings import BaseSettings


class SessionSettings(BaseSettings):
    """
    This class defines the setting configuration for this auth service
    """

    SESSION_ENGINE: str = Field(
        default="django.contrib.sessions.backends.cache",
        frozen=True,
    )
    SESSION_CACHE_ALIAS: str = Field(
        default="default",
        frozen=True,
    )
    SESSION_COOKIE_AGE: int = 1209600
    SESSION_COOKIE_SAMESITE: bool | str = "Lax"
    SESSION_COOKIE_HTTPONLY: bool = True


session_config = SessionSettings()
