from pathlib import Path, PosixPath

from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    BASE_DIR: PosixPath = Field(
        default=Path(__file__).resolve().parent.parent.parent,
        frozen=True,
    )
    ALLOWED_HOSTS: list[str] = ["*"]

    ROOT_URLCONF: str = "routes.urls"
    APPEND_SLASH: bool = False

    ASGI_APPLICATION: str = "config.server.asgi.application"
    money_to_point: PositiveInt = Field(default=200, frozen=True)
    point_to_money: PositiveInt = Field(default=1, frozen=True)


general_config = GeneralSettings()
