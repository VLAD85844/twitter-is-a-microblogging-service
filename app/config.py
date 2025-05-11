import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypass@localhost:5432/microblog_db")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

class Settings:
    DATABASE_URL: str = DATABASE_URL
    API_HOST: str = API_HOST
    API_PORT: int = API_PORT
    DEBUG: bool = DEBUG_MODE

settings = Settings()
