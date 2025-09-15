from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost/campus_ai"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    WHATSAPP_TOKEN: Optional[str] = None
    TELEGRAM_TOKEN: Optional[str] = None
    
    # Features
    ENABLE_OCR: bool = True
    ENABLE_VOICE: bool = True
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "mr", "ta", "te"]  # English, Hindi, Marathi, Tamil, Telugu
    
    # Thresholds
    CONFIDENCE_THRESHOLD: float = 0.7
    FALLBACK_THRESHOLD: float = 0.5
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"

settings = Settings()