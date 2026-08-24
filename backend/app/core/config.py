from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Real-Time CV Analytics"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@db:5432/cv_analytics"
    CAMERA_SOURCE: str = "0"
    CONFIDENCE_THRESHOLD: float = 0.5
    IOU_THRESHOLD: float = 0.45
    MODEL_NAME: str = "yolov8n.pt"
    MODEL_PATH: str = ""
    INPUT_WIDTH: int = 1280
    INPUT_HEIGHT: int = 720
    FPS_TARGET: int = 30
    DEVICE: str = "auto"
    FRAME_SKIP: int = 1
    MAX_TRACKING_AGE: int = 30
    MIN_HITS: int = 3


@lru_cache
def get_settings() -> Settings:
    return Settings()
