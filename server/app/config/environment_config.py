from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    GEMINI_API_KEY=GEMINI_API_KEY

    class Config:
        env_file = str(Path(__file__).resolve().parent / ".env")