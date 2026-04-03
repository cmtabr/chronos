from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from core.schemas.user import UserListQuery
from domain.repositories.user import UserRepository
from domain.services.user import UserService
from infrastructure.database.repositories.user import DBUserRepository
from infrastructure.database.session import get_session


def get_user_repository(
    session: Annotated[Session, Depends(get_session)],
) -> UserRepository:
    return DBUserRepository(session)


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository)


def get_user_list_query(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> UserListQuery:
    return UserListQuery(skip=skip, limit=limit)
