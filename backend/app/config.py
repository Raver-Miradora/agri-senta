from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Agri-Senta API"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str = "postgresql+asyncpg://agrisenta:password@localhost:5432/agrisenta"
    da_scrape_url: str = "https://www.da.gov.ph/price-monitoring/"
    psa_api_url: str = "https://openstat.psa.gov.ph/"
    scrape_schedule_cron: str = "0 6 * * *"
    forecast_schedule_cron: str = "0 0 * * 0"

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Auth
    secret_key: str = "dev-secret-change-in-production"
    access_token_expire_minutes: int = 60
    default_admin_username: str = "admin"
    default_admin_password: str = "admin123"

    # Rate limiting
    rate_limit_default: str = "60/minute"
    rate_limit_auth: str = "10/minute"


@lru_cache
def get_settings() -> Settings:
    return Settings()
