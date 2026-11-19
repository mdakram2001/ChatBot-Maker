from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # Application
    APP_NAME: str = "ChatAMU"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # LLM Configuration
    LLM_PROVIDER: str = "openrouter"
    LLM_MODEL: str = "openrouter/free"
    BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_API_KEY: str | None = None

    # Embedding Configuration
    EMBEDDING_MODEL: str = "Qwen/Qwen3-Embedding-0.6B"

    # Vector Database
    VECTOR_DB_PROVIDER: str = "chroma"
    CHROMA_DB_PATH: str = "./artifacts/chroma_db"

    # Crawler Configuration
    MAX_CRAWL_DEPTH: int = 3
    MAX_PAGES: int = 100
    REQUEST_TIMEOUT: int = 15
    MAX_RETRIES: int = 3

    # Text Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Logging
    LOG_LEVEL: str = "INFO"

    # API Keys
    PINECONE_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()