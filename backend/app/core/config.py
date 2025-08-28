import os
from typing import List

class Settings:
    PROJECT_NAME: str = "AI Chat API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS - Allow all origins for development, but can be restricted for production
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://127.0.0.1:3000",
        "https://127.0.0.1:3000",
        # Add ngrok URLs dynamically
        "https://*.ngrok.io",
        "https://*.ngrok-free.app",
        "https://*.ngrok.dev",
        # Allow all for development (remove in production)
        "*"
    ]
    
    # Chat settings
    MAX_MESSAGE_LENGTH: int = 1000
    MAX_MESSAGES_PER_SESSION: int = 100
    
    # TogetherAI settings
    TOGETHER_API_KEY: str = os.getenv('TOGETHER_API_KEY', '')

settings = Settings()