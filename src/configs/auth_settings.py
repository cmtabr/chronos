from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    """
    AuthSettings handles configuration settings for the environment.

    This class inherits from BaseSettings and utilizes pydantic for managing
    environment variables and settings. It reads configurations from an `.env` file.

    Attributes:
        `model_config` (SettingsConfigDict): Configuration for the settings model.
        `secret` (str): Secret key used on JWT signature
        `algorithm` (str | list[srt]): Algorithms used in JWT handling
    """

    model_config = SettingsConfigDict(
        env_prefix="AUTH_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    secret: str
    algorithm: str | list[str] = "HS256"
