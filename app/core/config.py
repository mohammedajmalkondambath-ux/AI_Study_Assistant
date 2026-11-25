
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration."""

    APP_NAME: str = "AI Study Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    GROQ_API_KEY: str = ""

    QDRANT_URL: str = "http://localhost:6333"
    MONGODB_URL: str = "mongodb://localhost:27017"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    EMBEDDING_MODEL: str = "BAAI/bge-m3"
    EMBEDDING_DIMENSION: int = 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
