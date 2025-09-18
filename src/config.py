import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file if available
load_dotenv()

class Settings(BaseSettings):
    # === Database ===
    USE_SQLITE: bool = os.getenv("USE_SQLITE", "true").lower() == "true"
    SQLITE_DB_URL: str = "sqlite:///./db.sqlite3"
    POSTGRES_DB_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/llmdb")

    # === LLM ===
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    USE_LLM_MOCK: bool = os.getenv("USE_LLM_MOCK", "false").lower() == "true"

    # === App ===
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ALLOWED_ORIGINS: list[str] = ["*"]
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")  # development, staging, production
    SECRET_KEY : str = os.getenv("SECRET_KEY", "supersecretkey")  # Change this in production!

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def DATABASE_URL(self):
        return self.SQLITE_DB_URL if self.USE_SQLITE else self.POSTGRES_DB_URL

settings = Settings()
