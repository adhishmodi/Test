from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = (
        "postgresql+asyncpg://traffic_app:dev_only_change_me@postgres:5432/traffic_monitor"
    )
    redis_url: str = "redis://redis:6379/0"
    rq_queue_name: str = "traffic"
    upload_dir: Path = Path("./var/uploads")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
