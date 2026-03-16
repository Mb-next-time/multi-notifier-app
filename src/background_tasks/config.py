from pydantic_settings import BaseSettings, SettingsConfigDict

class BrokerSettings(BaseSettings):
    PROTOCOL: str
    USERNAME: str
    PASSWORD: str
    HOSTNAME: str
    PORT: int

    model_config = SettingsConfigDict(env_file=".env.broker", env_prefix='BROKER_')
