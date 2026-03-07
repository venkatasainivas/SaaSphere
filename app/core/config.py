from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-this-in-production"
    FERNET_KEY: str = ""
    DATABASE_URL: str = "postgresql://postgres:Sainivas@localhost/saasphere"
    REDIS_URL: str = "redis://localhost:6379"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()