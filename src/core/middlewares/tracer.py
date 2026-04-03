from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.routers import TRACED_ROUTE_PREFIXES

logger = logging.getLogger(__name__)

trace_id_ctx: ContextVar[str | None] = ContextVar("chronos_trace_id", default=None)


def get_trace_id() -> str | None:
    """Trace id for the current request, when tracing is active for this path."""
    return trace_id_ctx.get()


def _path_matches_traced_prefixes(path: str) -> bool:
    return any(path == p or path.startswith(f"{p}/") for p in TRACED_ROUTE_PREFIXES)


class TracerMiddleware(BaseHTTPMiddleware):
    """
    Request tracing for HTTP operations served under `TRACED_ROUTE_PREFIXES`
    (routes mounted from `core.routers`).

    - Accepts optional `X-Trace-ID` header; otherwise generates one.
    - Exposes `request.state.trace_id` and contextvar `get_trace_id()`.
    - Sends `X-Trace-ID` on the response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        if not _path_matches_traced_prefixes(path):
            return await call_next(request)

        raw = request.headers.get("x-trace-id")
        trace_id = raw.strip() if raw and raw.strip() else uuid.uuid4().hex
        token = trace_id_ctx.set(trace_id)
        request.state.trace_id = trace_id
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            trace_id_ctx.reset(token)
            raise

        duration_ms = (time.perf_counter() - started) * 1000
        trace_id_ctx.reset(token)

        response.headers["X-Trace-ID"] = trace_id
        logger.info(
            "%s %s -> %s in %.2fms trace_id=%s",
            request.method,
            path,
            response.status_code,
            duration_ms,
            trace_id,
        )
        return response
