from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    DatabaseSettings handles database settings for the environment.

    This class inherits from BaseSettings and utilizes pydantic for managing
    environment variables and settings. It reads configurations from an `.env` file.

    Attributes:
        host (str): The database host.
        port (int): The database port.
        user (str): The database user.
        password (str): The database password.
        database (str): The database name.
        pool_size (int | None): The size of the connection pool. Default is 10.
        max_overflow (int | None): The maximum overflow size of the connection pool. Default is 20.
    """

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str
    port: int
    user: str
    password: str
    database: str

    pool_size: int = 10
    pool_recycle: int = 3600
    max_overflow: int = 20

    @property
    def connection_url(self) -> str:
        """Returns the url string for the database connection."""
        user = quote_plus(self.user)
        password = quote_plus(self.password)
        return f"postgresql+psycopg://{user}:{password}@{self.host}:{self.port}/{self.database}"
