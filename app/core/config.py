from pydantic_settings import BaseSettings
from typing import List
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    CORS_ALLOWED_ORIGINS: str = "http://localhost:4200,http://127.0.0.1:4200"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]

    class Config:
        from_attributes = True
        env_file = ".env"

settings = Settings()
