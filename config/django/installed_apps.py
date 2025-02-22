from pydantic import field_validator
from pydantic_settings import BaseSettings

from config.django.security import security_config
from config.env import EnvironmentChoices, env_config


class InstalledAppsSettings(BaseSettings):
    THIRD_PARTY_PACKAGE: list[str] = [
        "rest_framework",
        "rangefilter",
        "drf_spectacular",
        "corsheaders",
        "phonenumber_field",
        "taggit",
    ]

    LOCAL_APPS: list[str] = [
        "apps.user.apps.UserConfig",
        "apps.common.apps.CommonConfig",
        "apps.products.apps.ProductsConfig",
    ]

    INSTALLED_APPS: list[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        *THIRD_PARTY_PACKAGE,
        *LOCAL_APPS,
    ]

    @field_validator("INSTALLED_APPS", mode="after")
    def add_remove_apps(cls, value: list[str]) -> list[str]:
        match env_config.PROJECT_ENVIRONMENT:
            case EnvironmentChoices.LOCAL | EnvironmentChoices.LOCAL_CONTAINER:
                if security_config.DEBUG:
                    value = [
                        "debug_toolbar",
                    ] + value

                return value

            case EnvironmentChoices.TEST:
                value = [
                    "debug_toolbar",
                ] + value
                return value

            case EnvironmentChoices.DEV:
                if security_config.DEBUG:
                    value = [
                        "debug_toolbar",
                    ] + value

                return value

            case EnvironmentChoices.CI_CD:
                pass
                # value = (
                #     [
                #         "corsheaders",
                #     ]
                #     + value
                #     + ["phonenumber_field"]
                # )
                # return value

            case EnvironmentChoices.STAGING:
                pass

            case EnvironmentChoices.PRODUCTION:
                pass


installed_apps_config = InstalledAppsSettings()
