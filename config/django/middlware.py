from pydantic import field_validator
from pydantic_settings import BaseSettings

from config.django.security import security_config
from config.env import EnvironmentChoices, env_config


class MiddlewareSettings(BaseSettings):
    CUSTOM_MIDDLEWARE: list[str] = [
        "apps.common.middleware.url_validation_middleware.UrlValidationMiddleware",
    ]
    THIRD_PARTY_PACKAGE_MIDDLEWARE: list[str] = [
        "corsheaders.middleware.CorsMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
    MIDDLEWARE: list[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        *THIRD_PARTY_PACKAGE_MIDDLEWARE,
        *CUSTOM_MIDDLEWARE,
    ]

    @field_validator("MIDDLEWARE", mode="after")
    @classmethod
    def add_remove_middleware(cls, value: list[str]) -> list[str]:
        match env_config.PROJECT_ENVIRONMENT:
            case EnvironmentChoices.LOCAL | EnvironmentChoices.LOCAL_CONTAINER:
                if security_config.DEBUG:
                    value = [
                        "debug_toolbar.middleware.DebugToolbarMiddleware",
                    ] + value
                return value

            case EnvironmentChoices.TEST:
                pass

            case EnvironmentChoices.DEV:
                if security_config.DEBUG:
                    value = [
                        "debug_toolbar.middleware.DebugToolbarMiddleware",
                    ] + value
                # else:
                #     value = [
                #         "corsheaders.middleware.CorsMiddleware",
                #     ] + value
                return value

            case EnvironmentChoices.CI_CD:
                pass

            case EnvironmentChoices.STAGING:
                pass

            case EnvironmentChoices.PRODUCTION:
                pass


middleware_config = MiddlewareSettings()
