# Development Setup — Intelligent Traffic Monitoring System

This guide describes the initial Codespaces development environment. The P4 foundation batch provides the development container, PostgreSQL, Redis, environment template and Git ignore rules. Python/frontend dependency manifests and application entry points are added in later approved batches.

## Prerequisites

- GitHub account with Codespaces access.
- Docker support in the development environment.
- No local GPU is required for setup. GPU training/fine-tuning is planned for Google Colab.

## 1. Create the Codespace

1. Open the repository and select the `main` branch.
2. Select **Code → Codespaces → Create codespace**.
3. Wait for the development container to build.
4. The workspace, PostgreSQL and Redis services are started by Compose.

## 2. Configure local environment

From the repository root:

```bash
cp .env.example .env
```

The values in `.env.example` are development-only placeholders. Do not use them in a public deployment and do not commit `.env`.

## 3. Check supporting services

```bash
docker compose ps
docker compose exec postgres pg_isready -U traffic_app -d traffic_monitor
docker compose exec redis redis-cli ping
```

Expected checks: PostgreSQL reports that it is accepting connections and Redis responds with `PONG`.

The database and Redis are reachable from the workspace using the Compose hostnames `postgres` and `redis`.

## 4. Application commands (after later setup batches)

The following commands become available after the Python and frontend manifests and application entry points are added:

```bash
uv sync --group dev
cd frontend && npm ci
```

Backend and frontend start commands, Alembic migrations, RQ worker startup, health endpoints and automated test commands will be documented when their corresponding application components exist.

**Database note:** `DATABASE_DESIGN.md` is the authoritative logical schema. This setup batch does not create tables or migrations. Do not run `alembic upgrade head` until an approved initial migration is added.

## 5. Data and security precautions

- Keep real secrets in local environment files or the deployment secret manager, never in Git.
- PostgreSQL and Redis are internal Compose services and have no published host ports.
- Use only synthetic or appropriately licensed sample media during development.
- Do not commit datasets, uploaded footage, generated videos or model weights.
- Raw uploaded footage and webcam frames must not be retained by default, as required by the SRS.
- Temporary artifacts and retention cleanup require their own implementation and verification.

## 6. Troubleshooting

- If a service is still starting, run `docker compose ps` and inspect logs with `docker compose logs postgres` or `docker compose logs redis`.
- To stop services, run `docker compose down`.
- To stop services and delete the local database/Redis volumes, run `docker compose down -v`. **This permanently deletes local development data; use only when you intend to reset it.**
