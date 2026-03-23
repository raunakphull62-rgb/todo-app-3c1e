from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv('SUPABASE_URL')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()

def get_settings() -> Settings:
    return settings