from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os

# Load .env file explicitly
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    APP_NAME: str = 'RAINFO'
    VERSION: str = '1.0.0'
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ['*']
    ALERT_PIN: str = '1078'
    FAST2SMS_API_KEY: str = os.getenv('FAST2SMS_API_KEY', '')
    FIREBASE_SERVICE_ACCOUNT_PATH: str = os.getenv(
        'FIREBASE_SERVICE_ACCOUNT_PATH',
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'firebase-service-account.json'))
    )

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
