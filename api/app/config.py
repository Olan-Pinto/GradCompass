from typing import List
from decouple import config

class Settings:
    DATABASE_URL: str = config("DATABASE_URL")
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    ENVIRONMENT: str = config("ENVIRONMENT", default="development")
    GEMINI_API_KEY: str = config("GEMINI_API_KEY")
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = config(
        "ALLOWED_ORIGINS", 
        default="http://localhost:3000,http://127.0.0.1:3000",
        cast=lambda v: [s.strip() for s in v.split(",")]
    )

settings = Settings()