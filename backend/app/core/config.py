import re
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CRS API"
    app_env: str = "local"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    max_credits_per_term: int = 18
    credit_rate: int = 300
    rate_limit_per_minute: int = 120

    database_url: str
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    def get_database_url(self) -> str:
        """Convert Render's postgres:// URL to postgresql+psycopg://"""
        url = self.database_url
        if url.startswith("postgres://"):
            url = re.sub(r"^postgres://", "postgresql+psycopg://", url)
        elif url.startswith("postgresql://") and "+" not in url.split("://")[0]:
            url = re.sub(r"^postgresql://", "postgresql+psycopg://", url)
        return url


settings = Settings()
