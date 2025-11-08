from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VIDEO_SOURCE: str
    YOLO_MODEL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()