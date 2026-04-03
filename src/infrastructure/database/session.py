from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from configs.database_settings import DatabaseSettings

_database_settings = DatabaseSettings()


def create_engine_from_settings() -> Engine:
    return create_engine(
        _database_settings.connection_url,
        pool_size=_database_settings.pool_size,
        max_overflow=_database_settings.max_overflow,
        pool_recycle=_database_settings.pool_recycle,
    )


engine = create_engine_from_settings()
DBSession = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
