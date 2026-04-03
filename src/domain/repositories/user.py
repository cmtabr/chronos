import uuid
from abc import ABC, abstractmethod

from domain.models.user import UserModel


class UserRepository(ABC):
    """Contract for user persistence (port). Implementations are in the infrastructure."""

    @abstractmethod
    def create_user(self, user: UserModel) -> UserModel:
        """Create a new user."""
        ...

    @abstractmethod
    def get_user_by_id(self, user_id: uuid.UUID) -> UserModel:
        """Get a user by id.

        Raises:
            UserNotFoundError: se não existir usuário ativo com o id informado.
        """
        ...

    @abstractmethod
    def get_all_users(self) -> list[UserModel]:
        """Get all users."""
        ...

    @abstractmethod
    def update_user(self, user_id: uuid.UUID, user: UserModel) -> UserModel:
        """Update a user.

        Raises:
            UserNotFoundError: se não existir usuário ativo com o id informado.
        """
        ...

    @abstractmethod
    def delete_user(self, user_id: uuid.UUID) -> None:
        """Delete a user (soft delete).

        Raises:
            UserNotFoundError: se não existir usuário ativo com o id informado.
        """
        ...
