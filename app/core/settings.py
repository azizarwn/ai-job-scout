from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Job Scout"
    VERSION: str = "0.0.1"
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    TAVILY_API_KEY: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type:ignore
