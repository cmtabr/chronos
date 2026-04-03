import uuid

from domain.models.user import UserModel
from domain.repositories.user import UserRepository


class UserService:
    """Orchestrates user operations delegating persistence to the repository."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def create_user(self, user: UserModel) -> UserModel:
        """Create a new user."""
        return self._user_repository.create_user(user)

    def get_user_by_id(self, user_id: uuid.UUID) -> UserModel:
        """Get a user by id.

        Raises:
            UserNotFoundError: se não existir usuário ativo com o id informado.
        """
        return self._user_repository.get_user_by_id(user_id)

    def get_all_users(self) -> list[UserModel]:
        """Get all users."""
        return self._user_repository.get_all_users()

    def update_user(self, user_id: uuid.UUID, user: UserModel) -> UserModel:
        """Update a user.

        Raises:
            UserNotFoundError: se não existir usuário ativo com o id informado.
        """
        return self._user_repository.update_user(user_id, user)

    def delete_user(self, user_id: uuid.UUID) -> None:
        """Delete a user.

        Raises:
            UserNotFoundError: se não existir usuário ativo com o id informado.
        """
        return self._user_repository.delete_user(user_id)
