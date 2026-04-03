# Package metadata
__version__ = "1.0.0"
__author__ = "cmtabr"


# Package modules, submodules and functions importing

from core.routers.user.router import user_router

__all__ = ["user_router"]
