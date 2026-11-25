from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CareerMatch AI API"
    app_env: str = "development"
    secret_key: str = "change-me-in-development"
    database_url: str = "sqlite+pysqlite:///./careermatch.sqlite3"
    enable_semantic_matching: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

