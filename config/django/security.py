from pydantic import Field, PositiveInt, SecretStr, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyseto import Key
from pyseto.key_interface import KeyInterface

from config.env import EnvironmentChoices, env_config


class SecuritySettings(BaseSettings):
    SECRET_KEY: SecretStr = Field(frozen=True, alias="DJANGO_SECRET_KEY")
    DEBUG: bool = Field(default=False, frozen=True)
    TOKEN_EXPIRATION: PositiveInt = Field(
        default=60 * 60,
        frozen=True,
        alias="DJANGO_TOKEN_EXPIRATION",
    )

    WRAPPED_KEY_SECRET: SecretStr = Field(
        default="wdxvXJRPezMHayn6q6-JlhKtHPu2OEKKpNtOTuhKcYaor40-bycGsnyTnYDUTFSRMjnLndYSjmVeK1D3VQ-5CJwZ56oAdpr15kyi-spsTsHreKoI67WpdsyZF9jbFD4xsMmUyzU5MyjilIgILWLEPcx-LLFQNMC3ijxYPqEGcGE",
        frozen=True,
        repr=False,
        alias="DJANGO_WRAPPED_KEY_SECRET",
    )
    PEM_PRIVATE_KEY: SecretStr = Field(
        frozen=True,
        alias="DJANGO_PEM_PRIVATE_KEY",
        repr=False,
    )
    PEM_PUBLIC_KEY: SecretStr = Field(
        frozen=True,
        alias="DJANGO_PEM_PUBLIC_KEY",
        repr=False,
    )

    model_config = SettingsConfigDict(
        env_file=env_config.env_file,
        extra="ignore",
        case_sensitive=True,
    )

    @computed_field()
    def PRIVATE_KEY(self) -> KeyInterface:
        private_key_string = (
            "-----BEGIN PRIVATE KEY-----\n"
            + self.PEM_PRIVATE_KEY.get_secret_value()
            + "\n-----END PRIVATE KEY-----"
        )
        return Key.new(version=4, purpose="public", key=private_key_string)

    @computed_field()
    def PUBLIC_KEY(self) -> KeyInterface:
        public_key_string = (
            "-----BEGIN PUBLIC KEY-----\n"
            + self.PEM_PUBLIC_KEY.get_secret_value()
            + "\n-----END PUBLIC KEY-----"
        )
        return Key.new(version=4, purpose="public", key=public_key_string)

    @computed_field(repr=False)
    def secret_byte(self) -> bytes:
        return self.SECRET_KEY.get_secret_value().encode("utf-8")[:64]

    @computed_field()
    def SYMMETRIC_KEY(self) -> KeyInterface:
        wrapped_key = "k4.local-wrap.pie." + self.WRAPPED_KEY_SECRET.get_secret_value()
        return Key.from_paserk(
            wrapped_key,
            wrapping_key=self.secret_byte,
        )

    @field_validator("DEBUG", mode="after")
    def check_debug(cls, field: bool) -> bool:
        if env_config.PROJECT_ENVIRONMENT != EnvironmentChoices.PRODUCTION:
            return True
        return field


security_config = SecuritySettings()
