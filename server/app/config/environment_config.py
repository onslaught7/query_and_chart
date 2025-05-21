from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    GEMINI_API_KEY: str  
    GEMINI_LLM_MODEL: str
    OPENAI_API_KEY: str
    OPENAI_LLM_MODEL: str

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"  
        env_file_encoding = "utf-8"


settings = Settings()
