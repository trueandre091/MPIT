from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Основные настройки
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Template")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

    # API настройки
    API_PREFIX: str = "/api"
    DOCS_URL: str | None = "/docs" if DEBUG else None
    REDOC_URL: str | None = "/redoc" if DEBUG else None
    OPENAPI_URL: str | None = "/openapi.json" if DEBUG else None

    # Настройки сервера
    HOST: str = os.getenv("HOST", "localhost" if DEBUG else "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Настройки базы данных
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_db")

    # JWT настройки
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30" if DEBUG else "15"))

    # CORS настройки
    DEV_CORS_ORIGINS: str = os.getenv("DEV_CORS_ORIGINS", "http://localhost:3000")
    PROD_CORS_ORIGINS: str = os.getenv("PROD_CORS_ORIGINS", "https://your-production-domain.com")

    @property
    def allowed_origins(self) -> List[str]:
        """Получить список разрешенных origins в зависимости от окружения"""
        origins = self.DEV_CORS_ORIGINS if self.DEBUG else self.PROD_CORS_ORIGINS
        return [origin.strip() for origin in origins.split(",")]

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Получить настройки приложения (с кешированием)"""
    return Settings()