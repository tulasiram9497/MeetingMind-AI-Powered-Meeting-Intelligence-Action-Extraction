from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = 'development'
    database_url: str = 'sqlite:///./meetingmind.db'
    llm_api_key: str = ''
    llm_model: str = 'gpt-4o-mini'
    llm_base_url: str = ''
    embedding_model: str = 'all-MiniLM-L6-v2'
    max_upload_size_mb: int = 200
    cors_origins: str = 'http://localhost:5173'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)

    @property
    def cors_origins_list(self):
        return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / 'data' / 'uploads'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
VECTOR_DIR = BASE_DIR / 'data' / 'vector_store'

for directory in (UPLOAD_DIR, PROCESSED_DIR, VECTOR_DIR):
    directory.mkdir(parents=True, exist_ok=True)
