from pydantic_settings import BaseSettings, SettingsConfigDict

class CommonSettings(BaseSettings):
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env.common")

class DatabaseSettings(BaseSettings):
    DATABASE_ASYNC_DRIVER: str
    DATABASE_SYNC_DRIVER: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: int

    model_config = SettingsConfigDict(env_file=".env.database")

documentation_urls = {}
if not CommonSettings().DEBUG:
    documentation_urls.update({
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    })
