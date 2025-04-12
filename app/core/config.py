import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = 'Some app name'
    SERVICE_BASE_URL: str = '/someapp'
    SERVICE_LOCAL_HOST: str = 'localhost'
    SERVICE_LOCAL_PORT: int = 8080

    @property
    def SERVICE_SWAGGER_URL(self):
        return f'http://{self.SERVICE_LOCAL_HOST}:{settings.SERVICE_LOCAL_PORT}{self.SERVICE_BASE_URL}/schema/swagger'

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
