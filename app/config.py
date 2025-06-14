from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_NUMBER: str
    GOOGLE_DRIVE_FOLDER_ID: str
    GOOGLE_SHEETS_ID: str
    OPENAI_API_KEY: str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings() 