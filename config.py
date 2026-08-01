from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

setting_obj = Settings()
