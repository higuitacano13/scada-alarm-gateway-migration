from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


class Settings(BaseSettings):
    db_server: str
    db_name: str
    db_user: str
    db_password: str
    db_driver: str

    dataset_generated_path: Path
    dataset_processed_path: Path

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()