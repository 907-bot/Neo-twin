"""
NeoTwin — Configuration Management
Centralized settings for the entire application
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "NeoTwin"
    VERSION: str = "1.0.0"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 15  # Gemini free tier limit
    RATE_LIMIT_ENABLED: bool = True
    
    # Caching
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./data")
    MAX_FILE_SIZE_MB: int = 100
    
    # Model Configuration
    GEMINI_MODEL: str = "gemini-2.0-flash"
    CLIP_MODEL: str = "ViT-L/14"
    OWL_VIT_MODEL: str = "google/owlvit-large-patch14"
    SAM2_MODEL: str = "sam2_hiera_large"
    
    # Training
    COLMAP_PATH: str = os.getenv("COLMAP_PATH", "colmap")
    MAX_TRAINING_ITERATIONS: int = 30000
    
    # Monitoring
    ENABLE_MONITORING: bool = True
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
