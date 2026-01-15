"""Configuration module for Codeep AI SDK"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Codeep AI SDK"""

    # API Configuration
    API_BASE_URL: str = os.getenv("CODEEP_API_BASE_URL", "https://api.codeep.cc/v1")
    ENVIRONMENT: str = os.getenv("CODEEP_ENVIRONMENT", "production")

    @classmethod
    def get_base_url(cls) -> str:
        """Get the API base URL"""
        return cls.API_BASE_URL

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() == "development"

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() == "production"

    @classmethod
    def set_base_url(cls, url: str):
        """Set the API base URL"""
        cls.API_BASE_URL = url.rstrip("/")

    @classmethod
    def set_environment(cls, env: str):
        """Set the environment (development/production)"""
        cls.ENVIRONMENT = env.lower()

        # Auto-set URL based on environment
        if env.lower() == "development":
            cls.API_BASE_URL = "http://localhost:5001"
        elif env.lower() == "production":
            cls.API_BASE_URL = "https://api.codeep.cc/v1"


# Initialize configuration
config = Config()