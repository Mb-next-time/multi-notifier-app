from pydantic_settings import BaseSettings, SettingsConfigDict

class JwtSettings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env.api.jwt", env_prefix="JWT_")

