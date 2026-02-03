from pydantic_settings import BaseSettings, SettingsConfigDict

class JwtSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env.jwt")

