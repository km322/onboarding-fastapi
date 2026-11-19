from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Global settings, read from environment variables or backend/.env.

    The app refuses to start if a required setting is missing.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MONGODB_URI: str
    FRONTEND_ORIGIN: str


settings = Config()
