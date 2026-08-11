from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name : str = "borrex-backend"
    app_version : str = "1.0.0"

    debug : bool = True

    host : str = "127.0.0.1"
    port : int = 8000

    database_url : str
    algo : str
    app_secret_key : str 
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
