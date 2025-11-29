"""
Configuration module for Weather Application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration class"""
    
    # Weather API Configuration
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_API_BASE_URL = 'http://api.weatherapi.com/v1'
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Request Configuration
    REQUEST_TIMEOUT = 10  # seconds
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.WEATHER_API_KEY:
            raise ValueError(
                "WEATHER_API_KEY not found. Please set it in .env file. "
                "Get your free API key from: https://www.weatherapi.com/signup.aspx"
            )
