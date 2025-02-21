import inspect
import os
from typing import Any

from loguru import logger
from pydantic import SecretBytes, SecretStr
from pydantic import ValidationError as PydanticError
from pydantic_settings import BaseSettings

from config.django.auth import auth_config
from config.django.cache import cache_config
from config.django.channel import channel_config
from config.django.database import db_config
from config.django.general import general_config
from config.django.installed_apps import installed_apps_config
from config.django.location import location_config
from config.django.middlware import middleware_config
from config.django.rest_framework import drf_config
from config.django.schema import schema_config

# from settings.django.location import location_config
from config.django.security import security_config
from config.django.session import session_config
from config.django.static import static_config
from config.django.template import template_config


def to_django(settings: BaseSettings):
    stack = inspect.stack()
    parent_frame = stack[1][0]

    def _get_actual_value(val: Any):
        if isinstance(val, BaseSettings):
            # for DATABASES and other complicated objects
            return _get_actual_value(val.model_dump())
        elif isinstance(val, dict):
            return {k: _get_actual_value(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [_get_actual_value(item) for item in val]
        elif isinstance(val, SecretStr) or isinstance(val, SecretBytes):
            return val.get_secret_value()
        else:
            return val

    for key, value in settings.model_dump().items():
        parent_frame.f_locals[key] = _get_actual_value(value)


try:
    to_django(general_config)
    to_django(security_config)
    to_django(location_config)
    to_django(installed_apps_config)
    to_django(middleware_config)
    to_django(template_config)
    to_django(auth_config)
    to_django(db_config)
    to_django(channel_config)
    to_django(cache_config)
    to_django(session_config)
    to_django(static_config)
    to_django(drf_config)
    to_django(schema_config)

except PydanticError as error:
    logger.error(error.json())
    os._exit(500)
