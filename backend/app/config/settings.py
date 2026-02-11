from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Language Learning Platform"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/langdb"

    class Config:
        env_file = ".env"


settings = Settings()
