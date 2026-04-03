import uuid


class UserDomainError(Exception):
    """User domain exception base class"""


class UserNotFoundError(UserDomainError):
    """Unexisting or already removed user (soft delete)."""

    def __init__(self, user_id: uuid.UUID) -> None:
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")
