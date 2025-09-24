from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "MyMoney Expense Tracker"
    database_url: str = "sqlite:///./mymoney.db"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()﻿ 
