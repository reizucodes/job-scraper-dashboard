from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Job Scraper Dashboard API"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./job_scraper_dashboard.db"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="JSD_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
