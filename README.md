# Chronos

HTTP API built with **FastAPI**, **PostgreSQL**, and **Alembic** migrations. Code under `src/` is layered (**core**, **domain**, **infrastructure**) for routes/schemas, domain rules and models, and persistence details. Product documentation lives in a static site under **`docs/`** (Astro Starlight).

## Stack

| Area | Technology |
|------|------------|
| Runtime | Python 3.12+ (Docker image: 3.12) |
| API | FastAPI |
| Data | SQLAlchemy 2, psycopg, Pydantic / pydantic-settings |
| Migrations | Alembic (`migrations/`) |
| Local environment | Docker Compose (`compose.yml`), [uv](https://github.com/astral-sh/uv) |

## Repository layout

```text
.
├── compose.yml              # Services: Postgres + API
├── Makefile                 # setup, migration, migrate, dev, compose, …
├── pyproject.toml           # Dependencies and package metadata
├── uv.lock
├── migrations/              # Alembic (see migrations/README.md)
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
├── docs/                    # Documentation site (Starlight)
├── scripts/                 # create_enviroment_setup.sh, create_migration.sh
└── src/                     # Application (editable install)
    ├── main.py              # FastAPI app, middlewares, routers
    ├── Dockerfile           # API image used by Compose
    ├── configs/             # Settings (e.g. database, auth)
    ├── core/                # HTTP layer: routers, schemas, middlewares
    ├── domain/              # ORM models, services, repository contracts, exceptions
    ├── infrastructure/      # Implementations (DB session, repositories, …)
    └── utlis/               # Shared utilities (e.g. logging)
```

- **`core`**: exposes the API (routes in `core/routers/`, DTOs in `core/schemas/`).
- **`domain`**: domain rules and types (`domain/models`, `domain/services`, interfaces in `domain/repositories`).
- **`infrastructure`**: data access and external integrations without coupling them to HTTP routes.

## Quick start (development)

1. Install Python dependencies:

   ```bash
   uv sync
   ```

2. Create `.env` at the repo root (variables for Compose and settings):

   ```bash
   make setup
   ```

3. Start Postgres and the API:

   ```bash
   make dev
   ```

4. Apply database migrations (with Postgres published on `localhost:5432`, the default target is `POSTGRES_HOST=localhost`):

   ```bash
   make migrate
   ```

Interactive API docs are at `/api/v1/docs` (see `src/main.py`).

Useful commands: `make help`. Migrations: [`migrations/README.md`](migrations/README.md).

## Documentation (Starlight)

The repository documentation site lives in [`docs/`](docs/), using [Astro Starlight](https://starlight.astro.build/).

Requirements: Node.js (recommended: version in [`docs/.nvmrc`](docs/.nvmrc); with [nvm](https://github.com/nvm-sh/nvm): `cd docs && nvm use`).

```bash
cd docs
npm install
npm run dev
```

Static build (output in `docs/dist/`):

```bash
cd docs
npm run build
```
