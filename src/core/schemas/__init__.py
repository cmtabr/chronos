# Package metadata
__version__ = "1.0.0"
__author__ = "cmtabr"


# Package modules, submodules and functions importing

from core.schemas.user import (
    UserCreate,
    UserListQuery,
    UserRead,
    UserUpdate,
)

__all__ = [
    "UserCreate",
    "UserListQuery",
    "UserRead",
    "UserUpdate",
]
