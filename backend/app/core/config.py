import os
from typing import List

class Settings:
    PROJECT_NAME: str = "AI Chat API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]  # Configure appropriately for production
    
    # Chat settings
    MAX_MESSAGE_LENGTH: int = 1000
    MAX_MESSAGES_PER_SESSION: int = 100
    
    # TogetherAI settings
    TOGETHER_API_KEY: str = os.getenv('TOGETHER_API_KEY', '')

settings = Settings()