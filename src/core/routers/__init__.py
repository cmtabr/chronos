# Package metadata
__version__ = "1.0.0"
__author__ = "cmtabr"

# HTTP path prefixes for routes defined under this package. The tracer middleware
# only instruments requests matching one of these prefixes.
TRACED_ROUTE_PREFIXES: tuple[str, ...] = ("/api/v1",)

# Package modules, submodules and functions importing
