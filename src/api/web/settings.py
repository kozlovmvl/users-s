from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent.parent


class Settings(BaseSettings):
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
