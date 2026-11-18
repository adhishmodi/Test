from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Intelligent Traffic Monitoring API",
    version="0.1.0",
    description="API for image, video and webcam traffic analysis.",
    docs_url="/docs" if settings.app_env == "development" else None,
    redoc_url="/redoc" if settings.app_env == "development" else None,
)

app.include_router(health_router, prefix="/api/v1")
