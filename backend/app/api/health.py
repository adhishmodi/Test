from fastapi import APIRouter, Response, status
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def liveness() -> dict[str, str]:
    """Confirm that the API process is responding without exposing infrastructure."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(response: Response) -> dict[str, object]:
    """Check critical dependencies before the service accepts processing requests."""
    settings = get_settings()
    dependencies: dict[str, str] = {}

    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    redis_client = Redis.from_url(settings.redis_url, socket_connect_timeout=2)

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        dependencies["database"] = "ready"
    except Exception:
        dependencies["database"] = "unavailable"
    finally:
        await engine.dispose()

    try:
        await redis_client.ping()
        dependencies["queue"] = "ready"
    except Exception:
        dependencies["queue"] = "unavailable"
    finally:
        await redis_client.aclose()

    is_ready = all(value == "ready" for value in dependencies.values())
    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {"status": "ready" if is_ready else "not_ready", "dependencies": dependencies}
