from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auto-Heal Incident Bot API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    API_KEY: str = "change_me_in_env"

    DISCORD_WEBHOOK_URL: str = ""
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()