import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.exceptions.user import UserNotFoundError
from domain.models.user import UserModel
from domain.repositories.user import UserRepository


class DBUserRepository(UserRepository):
    """PostgreSQL/SQLAlchemy implementation of UserRepository (soft delete via deleted_at)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_user(self, user: UserModel) -> UserModel:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get_user_by_id(self, user_id: uuid.UUID) -> UserModel:
        stmt = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.deleted_at.is_(None),
        )
        user = self._session.scalar(stmt)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def get_all_users(self) -> list[UserModel]:
        stmt = select(UserModel).where(UserModel.deleted_at.is_(None))
        return list(self._session.scalars(stmt).all())

    def update_user(self, user_id: uuid.UUID, user: UserModel) -> UserModel:
        existing = self.get_user_by_id(user_id)
        existing.username = user.username
        existing.password = user.password
        existing.email = user.email
        existing.name = user.name
        existing.is_active = user.is_active
        existing.updated_at = datetime.now(timezone.utc)
        self._session.commit()
        self._session.refresh(existing)
        return existing

    def delete_user(self, user_id: uuid.UUID) -> None:
        stmt = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.deleted_at.is_(None),
        )
        existing = self._session.scalar(stmt)
        if existing is None:
            raise UserNotFoundError(user_id)
        existing.is_active = False
        existing.deleted_at = datetime.now(timezone.utc)
        self._session.commit()
