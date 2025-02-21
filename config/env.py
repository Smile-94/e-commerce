from enum import Enum

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentChoices(Enum):
    """
    Enum to define possible environments for the project.
    """

    LOCAL = "local"
    LOCAL_CONTAINER = "local_container"
    TEST = "test"
    DEV = "dev"
    CI_CD = "ci_cd"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvFileChoices(Enum):
    """
    Enum to map each environment to its corresponding .env file path.
    """

    LOCAL = "env/.env.local"
    LOCAL_CONTAINER = "env/.env.local_container"
    TEST = "env/.env.test"
    DEV = "env/.env.dev"
    CI_CD = "env/.env.ci_cd"
    STAGING = "env/.env.staging"
    PRODUCTION = "env/.env.prod"


class EnvSettings(BaseSettings):
    """
    EnvSettings class to define configuration settings for the environment,
    selecting the appropriate .env file based on the chosen environment.

    Fields:
    - PROJECT_ENVIRONMENT: Sets the current environment of the project,
      defaulting to `EnvironmentChoices.LOCAL`. This field is frozen, meaning
      it cannot be changed after initialization.

    Methods:
    - env_file: A computed property that returns the appropriate .env file path
      based on the value of `PROJECT_ENVIRONMENT`.

    model_config:
    - Sets the model configuration options, specifying that the default .env file
      should be named `.env`. Extra fields in .env files are ignored, and key
      matching is case-sensitive.
    """

    PROJECT_ENVIRONMENT: EnvironmentChoices = Field(
        default=EnvironmentChoices.LOCAL,  # Default environment set to LOCAL
        frozen=True,  # Makes this field immutable after initialization
    )

    @computed_field
    def env_file(self) -> str:
        """
        Computes the path to the environment file based on the selected
        `PROJECT_ENVIRONMENT`. This function matches each environment with
        its corresponding file path in `EnvFileChoices`.
        """

        match self.PROJECT_ENVIRONMENT:
            case EnvironmentChoices.LOCAL:
                return EnvFileChoices.LOCAL.value
            case EnvironmentChoices.LOCAL_CONTAINER:
                return EnvFileChoices.LOCAL_CONTAINER.value
            case EnvironmentChoices.TEST:
                return EnvFileChoices.TEST.value
            case EnvironmentChoices.DEV:
                return EnvFileChoices.DEV.value
            case EnvironmentChoices.CI_CD:
                return EnvFileChoices.CI_CD.value
            case EnvironmentChoices.STAGING:
                return EnvFileChoices.STAGING.value
            case EnvironmentChoices.PRODUCTION:
                return EnvFileChoices.PRODUCTION.value

    # Configuration settings for Pydantic
    model_config = SettingsConfigDict(
        env_file=(".env"),  # Default .env file location
        extra="ignore",  # Ignores extra keys not specified in the model
        case_sensitive=True,  # Keys are case-sensitive
    )


# Instantiate the environment configuration
env_config = EnvSettings()
