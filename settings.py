from pydantic_settings import BaseSettings # type: ignore

class Settings(BaseSettings):
    cors_allowed_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()