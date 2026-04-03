FROM python:3.12-slim-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev

FROM python:3.12-slim-bookworm AS runtime

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --no-log-init --create-home app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH" \
    VIRTUAL_ENV="/app/.venv"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml /app/uv.lock /app/README.md ./
COPY --from=builder /app/src ./src

RUN chown -R app:app /app

USER app
