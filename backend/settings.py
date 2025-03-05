from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "152364")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "easy_db")
    DB_CREATED: bool = os.getenv("DB_CREATED", "false").lower() == "true"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    TOKEN_EXPIRE_MINUTES: int = int(os.getenv("TOKEN_EXPIRE_MINUTES", 5))

    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MEDIA_ROOT: str = os.path.join(BASE_DIR, "media")
    MEDIA_URL: str = "/media/"

@lru_cache
def get_settings():
    return Settings()



    
    
    
