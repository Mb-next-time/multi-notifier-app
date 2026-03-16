import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

class CommonSettings(BaseSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"

    model_config = SettingsConfigDict(env_file=".env.api.common")

class DatabaseSettings(BaseSettings):
    ASYNC_DRIVER: str
    SYNC_DRIVER: str
    USERNAME: str
    PASSWORD: str
    HOST: str
    DATABASE: str
    PORT: int

    model_config = SettingsConfigDict(env_file=".env.api.database", env_prefix="DATABASE_")

documentation_urls = {}

common_settings = CommonSettings()

if not common_settings.DEBUG:
    documentation_urls.update({
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    })

logger = logging.getLogger()
logger.setLevel(level=common_settings.LOG_LEVEL)
