from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.middlewares import TracerMiddleware
from core.routers.user.router import user_router
from domain.exceptions.user import UserNotFoundError

app = FastAPI(
    title="Chronos API",
    version="0.1.0",
    docs_url="/api/v1/docs",
)

app.add_middleware(TracerMiddleware)
app.include_router(user_router)


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    _request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"User not found: {exc.user_id}"},
    )
