from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VIDEO_SOURCE: str
    YOLO_MODEL: str
    ALARM_COOLDOWN_SECONDS: float
    ZONES_FILE: str
    OUTPUT_PATH: str
    CONFIDENCE: float

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()