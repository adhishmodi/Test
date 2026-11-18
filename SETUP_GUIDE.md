# Development Setup — Intelligent Traffic Monitoring System

This guide describes the initial Codespaces environment and application scaffold.

## Prerequisites

- GitHub account with Codespaces access.
- Docker support in the development container.
- Python 3.12, Node.js 26, uv, npm and Docker CLI are provided by the Codespaces environment.
- No local GPU is required; GPU-dependent fine-tuning is planned for Google Colab.

## 1. Create the Codespace

1. Open the repository and select the `main` branch.
2. Select **Code → Codespaces → Create codespace**.
3. Wait for the development container to build.
4. The workspace, PostgreSQL and Redis services are started by Compose.

## 2. Configure environment

From the repository root:

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

The values are development-only placeholders. Never commit either `.env` file or use the sample credentials in a public deployment.

## 3. Install dependencies

```bash
cd backend
uv sync --group dev
cd ../frontend
npm install
```

The first install resolves dependencies and generates `backend/uv.lock` and `frontend/package-lock.json`. Commit both lock files with dependency changes. Subsequent installs should use the lock files (`uv sync --locked --group dev` and `npm ci`).

ML framework/model packages are intentionally not included yet. The detector, weights, tracking implementation and license review remain separate decisions.

## 4. Start supporting services

From the repository root:

```bash
docker compose ps
docker compose exec postgres pg_isready -U traffic_app -d traffic_monitor
docker compose exec redis redis-cli ping
```

Expected checks: PostgreSQL reports that it is accepting connections and Redis responds with `PONG`.

## 5. Run the backend

In a terminal:

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Liveness: `GET /api/v1/health`
- Readiness: `GET /api/v1/health/ready`
- Development API docs: `/docs`

Readiness checks PostgreSQL and Redis. It returns HTTP 503 if either dependency is unavailable.

## 6. Run the frontend

In another terminal:

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

Open the forwarded Vite port (5173). Vite proxies `/api` requests to the FastAPI service on port 8000.

The current dashboard is a UI scaffold only; image/video submission, job processing, tracking and analytics are not implemented yet.

## 7. Run checks

```bash
cd backend
uv run ruff check .
uv run pytest
cd ../frontend
npm run typecheck
npm run build
```

## 8. Database and data precautions

- `DATABASE_DESIGN.md` is the authoritative logical schema.
- This batch does not create SQLAlchemy models, Alembic migrations or database tables. Do not run `alembic upgrade head` yet.
- PostgreSQL and Redis are internal Compose services; their ports are not published to the host.
- Use only synthetic or appropriately licensed sample media.
- Do not commit datasets, uploads, generated videos or model weights.
- Raw uploaded footage and webcam frames must not be retained by default.
- Temporary artifact retention and deletion guarantees require separate implementation and verification.

## 9. Troubleshooting

- Inspect service state with `docker compose ps`.
- Inspect logs with `docker compose logs postgres` or `docker compose logs redis`.
- Stop services with `docker compose down`.
- `docker compose down -v` deletes local database and Redis data permanently; use only when intentionally resetting the environment.
