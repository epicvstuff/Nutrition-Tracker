from pydantic_settings import BaseSettings
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Nutrition Tracker API"
    
    # Model Settings
    MODEL_TYPE: str = "cnn"  # Can be "cnn" or "llm" in the future
    MODEL_PATH: str = "models/fruit_vegetable_classifier.h5"
    IMG_WIDTH: int = 150
    IMG_HEIGHT: int = 150
    
    # Server Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 