import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FoodWise AI - Smart Food Waste Management & Redistribution"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "foodwise_super_secret_jwt_key_2026_mofpi_smart_redistribution")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database: Supports SQLite for zero-config run, or PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./foodwise.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
    
    # IoT MQTT Broker settings (simulated or remote)
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "broker.hivemq.com")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", 1883))
    MQTT_TOPIC_SENSORS: str = "foodwise/sensors/#"
    
    # ML Models path
    ML_MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "trained_models")
    
    # File upload directory for food quality inspection
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.ML_MODEL_PATH, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
