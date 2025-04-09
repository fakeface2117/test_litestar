import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_LOCAL_HOST: str = 'localhost'
    SERVICE_LOCAL_PORT: int = 8080

    DRIVER: str = "postgresql+asyncpg"

    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')
    DB_NAME: str = os.getenv('DB_NAME')

    @property
    def DB_CONNECTION_STRING(self):
        return f"{self.DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
