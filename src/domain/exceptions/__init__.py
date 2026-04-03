# Package metadata
__version__ = "1.0.0"
__author__ = "cmtabr"


# Package modules, submodules and functions importing
from domain.exceptions.user import UserNotFoundError

__all__ = ["UserNotFoundError"]
