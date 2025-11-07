from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    BOT_TOKEN: str = ""
    WEBHOOK_URL: Optional[str] = None
    WEBHOOK_PATH: str = "/telegram"
    
    DATABASE_URL: str = ""
    
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    LOG_LEVEL: str = "INFO"
    

settings = Settings()
