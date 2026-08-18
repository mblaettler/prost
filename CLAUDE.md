# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is PROST

**PaRty Ordering SysTem** — a web app where bar staff order drink restocks and deliverers fulfill those orders. Three roles: `admin`, `bar`, and `deliverer`.

## Commands

### Backend (Python / FastAPI)

`pyproject.toml`/`poetry.lock` live at the repo root; the source (`api/`, `models/`) lives under `backend/`. Internal imports are absolute (`from api...`, `from models...`), so commands must run with `backend/` as the working directory, using the Poetry environment from the repo root:

```sh
cd backend && poetry run uvicorn api.main:app --reload   # dev server on :8000
```

Create the first admin user (CLI entrypoint in `backend/api/main.py`):

```sh
cd backend && poetry run python -m api.main <username> <password>
```

The API docs are available at `http://localhost:8000/docs` when the dev server is running.

### Frontend (Vue 3 / Vite)

Run from the `ui/` directory:

```sh
npm install          # install dependencies
npm run dev          # dev server on :5173
npm run build        # type-check + compile
npm run type-check   # vue-tsc only
npm run lint         # oxlint then eslint (both --fix)
npm run format       # prettier over src/
```

There are no tests configured yet (`npm test` has no runner).

## Architecture

The backend source lives under `backend/`, while `pyproject.toml`/`poetry.lock` stay at the repo root (see [Commands](#backend-python--fastapi) above).

- **`backend/models/`** — SQLAlchemy ORM layer. `models/database.py` defines the `Base` class. Each model (User, Product, ProductCategory, ProductState) lives in its own file under `models/config/` or `models/order/`.
- **`backend/api/`** — FastAPI application. `api/main.py` wires together all routers and runs `Base.metadata.create_all` on startup (SQLite at `./prost.db` by default, overridable via `DATABASE_URL` env var).
- **`backend/api/auth.py`** — JWT auth (HS256, 30-min expiry). `SECRET_KEY` must be set as an env var. Exports dependency functions `verify_admin`, `verify_bar`, and `verify_deliverer` that protect routers via FastAPI `Depends`.
- **`backend/api/schemas.py`** — Pydantic schemas (input/output). Separate from ORM models to avoid leaking `password_hash`.
- **`backend/api/config/`** — Admin-only CRUD routers for users, products, and product categories (all prefixed `/config/…`, all require `verify_admin`).
- **`backend/api/bar/`** — Bar role endpoints (`/bar/product/…`). Reading product states merges DB rows with all products (missing rows default to `ENOUGH`).
- **`backend/api/deliverer/`** — Deliverer role endpoints (`/deliverer/product/…`). Shows all non-`ENOUGH` states across all bars.

### Data model

`ProductState` has a composite primary key `(product_id, bar_id)` and a `status` of `ENOUGH | REQUIRED | EMERGENCY`. A missing row is treated as `ENOUGH` — states are created on first write.

### Frontend

- **`ui/src/api.ts`** — Single API client object (`api`). Stores the JWT in `localStorage` and decodes the role from it client-side. All fetch calls go through `api.fetch()` which injects the `Authorization` header.
- **`ui/src/router/index.ts`** — Role-based routing guard: unauthenticated users are redirected to `/login`; authenticated users are redirected to their role's route if they hit the wrong one.
- **`ui/src/views/`** — Three role areas (`admin/`, `bar/`, `deliverer/`) plus `LoginView`. Layout shells (`AdminLayout`, `BarLayout`, `DelivererLayout`) are in `components/`.
- **`ui/src/types.ts`** — Shared TypeScript interfaces mirroring the backend Pydantic schemas.

### Frontend code style

- Single quotes, semicolons, 2-space indent (enforced by Prettier + oxlint/eslint).
- Vue 3 Composition API with `<script setup>`.
- Tailwind CSS for styling.

### Docker

- **`backend/Dockerfile`** — builds from the repo root as build context (installs Poetry deps from the root `pyproject.toml`/`poetry.lock`, then copies `backend/api/` and `backend/models/` in). Serves on `:8000`.
- **`ui/Dockerfile`** — multi-stage build from the `ui/` directory (Vite build, then served via nginx). Serves on `:80`.